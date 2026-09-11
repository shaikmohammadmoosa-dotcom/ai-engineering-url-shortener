from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class URLCreate(BaseModel):
    target_url: HttpUrl
    custom_code: Optional[str] = Field(None, min_length=3, max_length=10)
    ttl_days: Optional[int] = Field(30, ge=1, le=365)


class URLResponse(BaseModel):
    short_code: str
    short_url: str
    target_url: str
    created_at: datetime
    expires_at: Optional[datetime]


class AnalyticsResponse(BaseModel):
    short_code: str
    target_url: str
    click_count: int
    created_at: datetime
    last_accessed: Optional[datetime]