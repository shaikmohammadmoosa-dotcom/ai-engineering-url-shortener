from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse

from app.config import settings
from app.database import db
from app.models import URLCreate, URLResponse, AnalyticsResponse
from app.shortener import generate_short_code

app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description="Production-grade AI-assisted URL shortener service",
)


@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    return {"status": "ok", "version": settings.app.version}


@app.post(
    "/shorten",
    response_model=URLResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["URL Shortener"],
)
def create_short_url(payload: URLCreate) -> Dict[str, Any]:
    target_url_str = str(payload.target_url)

    if payload.custom_code:
        short_code = payload.custom_code
    else:
        short_code = generate_short_code(
            target_url_str, length=settings.shortener.code_length
        )

    created_at = datetime.now(timezone.utc)
    ttl = payload.ttl_days or settings.shortener.default_ttl_days
    expires_at = created_at + timedelta(days=ttl)

    success = db.save_url(short_code, target_url_str, created_at, expires_at)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Short code already exists or database error.",
        )

    short_url = f"{settings.app.base_url}/{short_code}"
    return {
        "short_code": short_code,
        "short_url": short_url,
        "target_url": target_url_str,
        "created_at": created_at,
        "expires_at": expires_at,
    }


@app.get("/{short_code}", tags=["URL Shortener"])
def redirect_to_url(short_code: str):
    record = db.get_url(short_code)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
        )

    if record.get("expires_at"):
        expires = datetime.fromisoformat(record["expires_at"])
        if datetime.now(timezone.utc) > expires:
            raise HTTPException(
                status_code=status.HTTP_410_GONE, detail="Short URL has expired"
            )

    return RedirectResponse(
        url=record["target_url"], status_code=status.HTTP_302_FOUND
    )


@app.get(
    "/analytics/{short_code}",
    response_model=AnalyticsResponse,
    tags=["Analytics"],
)
def get_analytics(short_code: str) -> Dict[str, Any]:
    record = db.get_analytics(short_code)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
        )

    return {
        "short_code": record["short_code"],
        "target_url": record["target_url"],
        "click_count": record["click_count"],
        "created_at": datetime.fromisoformat(record["created_at"]),
        "last_accessed": (
            datetime.fromisoformat(record["last_accessed"])
            if record.get("last_accessed")
            else None
        ),
    }