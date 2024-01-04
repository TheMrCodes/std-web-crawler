from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from std_web_crawler.db.base import BaseModel



@dataclass
class Url(BaseModel):
    __incomplete_tablename__ = 'urls'

    # Fields
    id: int
    url: str
    lastmod: datetime
    crawled_at: Optional[datetime]
    created_at: datetime

    # Mapped Fields
    id: Mapped[int]                             = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str]                            = mapped_column(String(2000), nullable=False)
    lastmod: Mapped[datetime]                   = mapped_column(DateTime, nullable=False)
    crawled_at: Mapped[Optional[datetime]]      = mapped_column(DateTime, nullable=True, default=None)
    created_at: Mapped[datetime]                = mapped_column(DateTime, nullable=False)
