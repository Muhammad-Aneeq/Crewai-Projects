from typing import List, Optional
from pydantic import BaseModel

class ChapterOutline(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class BookOutline(BaseModel):
    chapters: List[ChapterOutline] = []

class Chapter(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
