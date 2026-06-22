from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsResponse(BaseModel):
    id: int
    title: str
    link: str
    published : Optional[datetime] = None