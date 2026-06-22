import aiohttp
import feedparser
from typing import List, Dict
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime

from app.models.news import News


async def fetch_news(url: str) -> List[Dict[str, str]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            d = feedparser.parse(text)

            result = []
            for entry in d['entries']:
                title = entry.get('title', '')
                link = entry.get('link', '')
                result.append({"title": title, "link": link})
            return result


def save_news_to_db(news: List[Dict[str, str]], db: Session):
    for item in news:
        link = item["link"]

        # если уже есть
        existing = db.query(News).filter(News.link == link).first()

        # Если нет - создаем новую
        if not existing:
            new_news = News(
                title=item["title"],
                link=link,
                published=datetime.now()
            )
            db.add(new_news)

    db.commit()