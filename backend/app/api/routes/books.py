"""
Books API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.schemas.book import BookListResponse

router = APIRouter()


@router.get("", response_model=List[BookListResponse])
async def get_books(
    reading_level_min: Optional[float] = Query(None, description="Minimum reading level"),
    reading_level_max: Optional[float] = Query(None, description="Maximum reading level"),
    db: Session = Depends(get_db)
):
    """
    Get list of all books with optional filtering by reading level.
    
    Args:
        reading_level_min: Optional minimum reading level filter
        reading_level_max: Optional maximum reading level filter
        db: Database session
        
    Returns:
        List of books with id, title, author, reading_level, and total_words
    """
    try:
        query = db.query(Book)
        
        # Apply reading level filters if provided
        if reading_level_min is not None:
            query = query.filter(Book.reading_level >= reading_level_min)
        
        if reading_level_max is not None:
            query = query.filter(Book.reading_level <= reading_level_max)
        
        books = query.all()
        
        return [
            BookListResponse(
                id=book.id,
                title=book.title,
                author=book.author,
                reading_level=book.reading_level,
                total_words=book.total_words
            )
            for book in books
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching books: {str(e)}"
        )
