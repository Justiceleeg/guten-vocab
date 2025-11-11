"""
Pydantic schemas for book API responses.
"""
from typing import Optional
from pydantic import BaseModel


class BookListResponse(BaseModel):
    """Book list item."""
    id: int
    title: str
    author: Optional[str] = None
    reading_level: Optional[float] = None
    total_words: Optional[int] = None

    class Config:
        from_attributes = True

