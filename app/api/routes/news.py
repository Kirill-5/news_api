from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session
from typing import List

from app.services.parser import fetch_news, save_news_to_db
from app.db.database import get_db
from app.models.news import News
from app.schemas.news import NewsResponse


router = APIRouter(prefix="/news", tags=["news"])

@router.get("/news", response_model=List[NewsResponse])
@cache(expire=300)  # 5 минут
async def get_news(url: str, db: Session = Depends(get_db)):
    news = await fetch_news(url)
    save_news_to_db(news, db)
    all_news = db.query(News).all()
    return all_news