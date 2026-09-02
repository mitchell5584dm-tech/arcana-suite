"""Offline-first evidence inventory and chain-of-custody services."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import uuid
from pathlib import Path
from typing import Iterable

from .models import EvidenceRecord, TargetPlatform, utc_now

CASE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


class EvidenceService:
    """Persist cases and immutable evidence metadata in a local SQLite store.

    EVIDRYX never modifies or uploads source evidence. Files are opened read-only,
    hashed in chunks, and represented by metadata suitable for later analysis.
    """

    def __init__(self, database: str | Path, allowed_roots: Iterable[str | Path] | None = None):
        self.database = Path(database)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        roots = allowed_roots or [Path.cwd()]
        self.allowed_roots = tuple(Path(root).resolve() for root in roots)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=10.0)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        return connection

    def _initialize(self) -> None:
        with self._connect() as db:
            db.execute("PRAGMA journal_mode = WAL")
            db.execute("PRAGMA synchronous = FULL")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS cases (
                    case_id TEXT PRIMARY KEY, name TEXT NOT NULL,
                    description TEXT NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS evidence (
                    evidence_id TEXT PRIMARY KEY, case_id TEXT NOT NULL,
                    source_path TEXT NOT NULL, display_name TEXT NOT NULL,
                    platform TEXT NOT NULL, sha256 TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL, acquired_at TEXT NOT NULL,
                    acquisition_method TEXT NOT NULL, examiner TEXT NOT NULL,
                    FOREIGN KEY(case_id) REFERENCES cases(case_id)
                );
                CREATE TABLE IF NOT EXISTS audit_events (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT, occurred_at TEXT NOT NULL,
                    action TEXT NOT NULL, subject_id TEXT NOT NULL, details TEXT NOT NULL,
                    previous_hash TEXT NOT NULL, event_hash TEXT NOT NULL UNIQUE
                );
            """)

    @staticmethod
    def _validate_case_id(case_id: str) -> str:
        if not CASE_ID_PATTERN.fullmatch(case_id):
            raise ValueError("case_id must be 1-64 safe alphanumeric, dot, dash, or underscore characters")
        return case_id

    def _safe_source(self, source_path: str | Path) -> Path:
        path = Path(source_path).resolve(strict=True)
        if not path.is_file():
            raise ValueError("evidence source must be a regular file")
        if not any(path == root or root in path.parents for root in self.allowed_roots):
            raise PermissionError("evidence source is outside configured allowed roots")
        return path

    @staticmethod
    def hash_file(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _audit(self, db: sqlite3.Connection, action: str, subject_id: str, details: dict) -> None:
        previous = db.execute(
            "SELECT event_hash FROM audit_events ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        previous_hash = previous[0] if previous else "0" * 64
        occurred_at = utc_now()
        canonical = json.dumps(details, sort_keys=True, separators=(",", ":"))
        payload = "|".join((previous_hash, occurred_at, action, subject_id, canonical))
        event_hash = hashlib.sha256(payload.encode()).hexdigest()
        db.execute(
            "INSERT INTO audit_events (occurred_at, action, subject_id, details, previous_hash, event_hash) VALUES (?, ?, ?, ?, ?, ?)",
            (occurred_at, action, subject_id, canonical, previous_hash, event_hash),
        )

    def create_case(self, case_id: str, name: str, description: str = "") -> dict:
        case_id = self._validate_case_id(case_id)
        if not name.strip():
            raise ValueError("case name is required")
        created_at = utc_now()
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT INTO cases VALUES (?, ?, ?, ?)", (case_id, name.strip(), description, created_at))
            self._audit(db, "case.created", case_id, {"name": name.strip()})
        return {"case_id": case_id, "name": name.strip(), "description": description, "created_at": created_at}

    def register_evidence(self, *, case_id: str, source_path: str | Path,
                          platform: str, examiner: str, acquisition_method: str) -> EvidenceRecord:
        case_id = self._validate_case_id(case_id)
        try:
            normalized_platform = TargetPlatform(platform.lower()).value
        except ValueError as error:
            raise ValueError("platform must be windows, linux, or android") from error
        if not examiner.strip() or not acquisition_method.strip():
            raise ValueError("examiner and acquisition_method are required")
        path = self._safe_source(source_path)
        digest = self.hash_file(path)
        record = EvidenceRecord(
            evidence_id=str(uuid.uuid4()), case_id=case_id, source_path=str(path),
            display_name=path.name, platform=normalized_platform, sha256=digest,
            size_bytes=path.stat().st_size, acquired_at=utc_now(),
            acquisition_method=acquisition_method.strip(), examiner=examiner.strip(),
        )
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            if not db.execute("SELECT 1 FROM cases WHERE case_id = ?", (case_id,)).fetchone():
                raise LookupError(f"case not found: {case_id}")
            db.execute(
                "INSERT INTO evidence VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                tuple(record.to_dict().values()),
            )
            self._audit(db, "evidence.registered", record.evidence_id,
                        {"case_id": case_id, "sha256": digest, "size_bytes": record.size_bytes})
        return record

    def verify_evidence(self, evidence_id: str) -> dict:
        with self._connect() as db:
            row = db.execute("SELECT * FROM evidence WHERE evidence_id = ?", (evidence_id,)).fetchone()
            if not row:
                raise LookupError(f"evidence not found: {evidence_id}")
            path = self._safe_source(row["source_path"])
            actual = self.hash_file(path)
            verified = actual == row["sha256"] and path.stat().st_size == row["size_bytes"]
            db.execute("BEGIN IMMEDIATE")
            self._audit(db, "evidence.verified", evidence_id, {"verified": verified, "actual_sha256": actual})
        return {"evidence_id": evidence_id, "verified": verified, "expected_sha256": row["sha256"], "actual_sha256": actual}

    def audit_log(self) -> list[dict]:
        with self._connect() as db:
            return [dict(row) for row in db.execute("SELECT * FROM audit_events ORDER BY sequence")]

    def verify_audit_chain(self) -> bool:
        previous = "0" * 64
        for event in self.audit_log():
            payload = "|".join((previous, event["occurred_at"], event["action"], event["subject_id"], event["details"]))
            if event["previous_hash"] != previous or hashlib.sha256(payload.encode()).hexdigest() != event["event_hash"]:
                return False
            previous = event["event_hash"]
        return True
