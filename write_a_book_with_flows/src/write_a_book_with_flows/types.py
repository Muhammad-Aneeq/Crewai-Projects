from typing import List
from pydantic import BaseModel

class ChapterOutline(BaseModel):
    title: str | None = None
    description: str | None = None

class BookOutline(BaseModel):
    chapters: List[ChapterOutline] = []


class Chapter(BaseModel):
    title: str | None = None
    content: str | None = None