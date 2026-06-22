from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String, unique=True)
    published = Column(DateTime, nullable=True)