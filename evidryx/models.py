"""Domain models shared by the EVIDRYX service and API."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class TargetPlatform(str, Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    ANDROID = "android"


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    case_id: str
    source_path: str
    display_name: str
    platform: str
    sha256: str
    size_bytes: int
    acquired_at: str
    acquisition_method: str
    examiner: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
