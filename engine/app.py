# engine/app.py
import asyncio
import time
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import aiofiles

from engine.cache import cached
from engine.logging_config import log_request
from engine.analytics import parse_logs

app = FastAPI(
    title="Arcana Suite",
    version="1.0.0",
    description="Automated OSINT + mobile forensics toolkit backend.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    response: Response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    await log_request(request, response.status_code, elapsed_ms)
    return response


async def fetch_osint(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [client.get(u) for u in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        results = []
        for r in responses:
            if isinstance(r, Exception):
                results.append({"error": str(r)})
            else:
                results.append(
                    {
                        "url": str(r.url),
                        "status": r.status_code,
                        "body": r.text[:2048],
                    }
                )
        return results


async def read_artifact(path: str) -> str:
    async with aiofiles.open(path, "r") as f:
        return await f.read()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/osint")
async def osint_endpoint(q: str):
    urls = [
        f"https://example-osint-source1.com/search?q={q}",
        f"https://example-osint-source2.com/search?q={q}",
    ]
    start = time.perf_counter()
    results = await cached(f"osint:{q}", 300, fetch_osint, urls)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return {
        "query": q,
        "results": results,
        "elapsed_ms": elapsed_ms,
        "cached": True,
    }


@app.get("/artifact")
async def artifact_endpoint(path: str):
    content = await read_artifact(path)
    return {
        "path": path,
        "size": len(content),
    }


@app.get("/dashboard/analytics")
async def analytics_dashboard():
    data = parse_logs(limit=2000)
    return {
        "summary": {
            "total_lines": data.get("lines_parsed", 0),
        },
        "methods": data.get("methods", {}),
        "paths": data.get("paths", {}),
        "statuses": data.get("statuses", {}),
    }
