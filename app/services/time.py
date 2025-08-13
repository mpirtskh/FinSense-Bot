from __future__ import annotations

from datetime import datetime
from typing import Optional

try:
    from zoneinfo import ZoneInfo 
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


def get_current_time(timezone: Optional[str] = None) -> str:
    if timezone and ZoneInfo is not None:
        try:
            tz = ZoneInfo(timezone)
        except Exception:
            tz = None
    else:
        tz = None

    now = datetime.now(tz) if tz else datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S %Z").strip() 