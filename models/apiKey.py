from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional


class ApiKey(BaseModel):
    user: str
    key: str
    tier: int = Field(default=0)
    usageToday: int = 0
    usageTotal: int = 0
    date: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))
