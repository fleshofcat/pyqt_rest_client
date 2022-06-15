from typing import List, Optional

from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: Optional[str]


class Tag(BaseModel):
    id: int
    name: Optional[str]


class Pet(BaseModel):
    id: int
    name: Optional[str]
    status: Optional[str]
    category: Optional[Category]
    photoUrls: Optional[List[str]]
    tags: Optional[List[Tag]]
