# EVIDRYX production foundation

EVIDRYX is a defensive digital-forensics and incident-response application from
**Arcana Forensics**. This foundation preserves ARCANA Suite and introduces an
offline-first evidence service for Windows, Linux, and Android investigations.

## Security and evidence guarantees

- Source evidence is opened read-only and never uploaded or modified.
- Every registered item receives a streaming SHA-256 digest and UUID.
- Evidence paths must be inside an explicitly configured root.
- Cases and evidence metadata are stored locally in SQLite with foreign keys.
- Case creation, registration, and verification produce a hash-chained audit log.
- Verification re-reads the source and compares both its digest and byte length.
- Every endpoint except `/health` requires an API key in the `X-API-Key` header.
- The service fails closed when no key is configured and compares keys in constant time.
- Request bodies are capped before validation, and API errors do not expose paths,
  database messages, stack traces, or submitted values.
- SQLite uses WAL mode, full synchronization, a 10-second busy timeout, and
  immediate write transactions to serialize hash-chain updates.

This is an inventory and integrity foundation, not a forensic acquisition tool.
Examiners must use validated, lawful acquisition procedures and preserve original
media using appropriate write blockers.

## Run locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export EVIDRYX_DATA_DIR="$PWD/data"
export EVIDRYX_EVIDENCE_ROOTS="/evidence/read-only"
export EVIDRYX_API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export EVIDRYX_MAX_REQUEST_BYTES=1048576
uvicorn evidryx.api:app --host 127.0.0.1 --port 8000
```

Keep the default loopback binding unless authentication and transport security
are added at a trusted reverse proxy. Multiple evidence roots use the operating
system path separator (`:` on Linux, `;` on Windows).

`EVIDRYX_API_KEY` is required and must be supplied only through the deployment
environment or secret manager. Never put a real key in source control, a Render
blueprint, a URL, or application logs. Render marks this variable `sync: false`,
so an operator must provide it as a secret during deployment. If it is absent or
empty, protected routes—including `/docs` and `/openapi.json`—return HTTP 503.
Clients send the key as `X-API-Key`; invalid or missing keys return HTTP 401.

`EVIDRYX_MAX_REQUEST_BYTES` defaults to 1 MiB and is constrained to 1 KiB–10 MiB.
Reverse proxies should enforce an equal or smaller limit. The current API accepts
metadata and local paths, not evidence-file uploads.

## API workflow

Include `X-API-Key: <secret>` on every request below.

1. `POST /api/v1/cases` with `case_id`, `name`, and optional `description`.
2. `POST /api/v1/evidence` with the case, local source path, target platform,
   examiner, and acquisition method.
3. `POST /api/v1/evidence/{id}/verify` before and after analysis or transfer.
4. `GET /api/v1/audit/integrity` to validate the audit chain.

## Repository audit and changes

The audit found duplicated legacy snapshots and accidentally tracked Git-internal
files. They are retained in this foundation to avoid silently removing history or
ARCANA functionality. The canonical root application remains compatible. Future
work should migrate legacy modules into packages, add authenticated case access,
signed exports, database migrations, platform collectors, and retention controls.

No active collection, exploitation, persistence, remote execution, or credential
access capability is introduced by EVIDRYX.
