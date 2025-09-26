import os
import json
from pathlib import Path
from typing import Any, Dict

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com")
# Prefer stable, widely-available realtime models if env not set
REALTIME_MODEL = os.environ.get("REALTIME_MODEL", "gpt-realtime")

app = FastAPI()


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse({
        "status": "ok",
        "message": "Open /demo for the browser demo, or POST /ephemeral to mint a token."
    })


@app.get("/demo", response_class=HTMLResponse)
async def demo_page() -> HTMLResponse:
    # Serve the bundled demo HTML from the repository
    here = Path(__file__).resolve().parent
    html_path = here / "realtime_web_demo.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="Demo file not found")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.post("/ephemeral")
async def create_ephemeral() -> JSONResponse:
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")
    payload: Dict[str, Any] = {
        "model": REALTIME_MODEL,
        "voice": "verse",
        "instructions": "Keep responses concise."
    }
    async with httpx.AsyncClient(base_url=OPENAI_BASE_URL, timeout=15) as client:
        r = await client.post(
            "/v1/realtime/sessions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        if r.status_code >= 300:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        data = r.json()
        token = data.get("client_secret", {}).get("value")
        if not token:
            raise HTTPException(status_code=500, detail="Failed to mint ephemeral token")
        return JSONResponse({"client_secret": token})


# Run with: uv run --no-project --with fastapi --with "uvicorn[standard]" uvicorn realtime_ephemeral_server:app --port 5057

