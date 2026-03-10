from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from sqlalchemy.orm import Session

from models import Bookmark, SessionLocal
from ai_service import generate_tags, semantic_search

router = APIRouter(prefix="/api")

# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# Pydantic schemas – simple, no complex validators
# ---------------------------------------------------------------------------
class BookmarkBase(BaseModel):
    url: str = Field(..., min_length=1)
    title: str = Field(..., max_length=255)
    tags: Optional[List[str]] = Field(default_factory=list)

    @validator("tags", each_item=True)
    def tag_length(cls, v: str) -> str:
        if len(v) > 50:
            raise ValueError("Tag length must be <= 50 characters")
        return v

class BookmarkCreate(BookmarkBase):
    pass

class BookmarkUpdate(BaseModel):
    title: Optional[str] = None
    tags: Optional[List[str]] = None

class BookmarkRead(BookmarkBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ---------------------------------------------------------------------------
# CRUD Endpoints
# ---------------------------------------------------------------------------
@router.post("/bookmarks", response_model=BookmarkRead, status_code=status.HTTP_201_CREATED)
def create_bookmark(payload: BookmarkCreate, db: Session = Depends(get_db)) -> BookmarkRead:
    db_obj = Bookmark(url=payload.url, title=payload.title, tags=payload.tags or [])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/bookmarks", response_model=List[BookmarkRead])
def list_bookmarks(q: Optional[str] = None, db: Session = Depends(get_db)) -> List[BookmarkRead]:
    query = db.query(Bookmark)
    if q:
        like_q = f"%{q}%"
        query = query.filter(
            (Bookmark.title.ilike(like_q)) | (Bookmark.url.ilike(like_q))
        )
    return query.order_by(Bookmark.created_at.desc()).all()

@router.get("/bookmarks/{bookmark_id}", response_model=BookmarkRead)
def get_bookmark(bookmark_id: int, db: Session = Depends(get_db)) -> BookmarkRead:
    obj = db.get(Bookmark, bookmark_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return obj

@router.put("/bookmarks/{bookmark_id}", response_model=BookmarkRead)
def update_bookmark(bookmark_id: int, payload: BookmarkUpdate, db: Session = Depends(get_db)) -> BookmarkRead:
    obj = db.get(Bookmark, bookmark_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    if payload.title is not None:
        obj.title = payload.title
    if payload.tags is not None:
        obj.tags = payload.tags
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/bookmarks/{bookmark_id}", response_class=JSONResponse)
def delete_bookmark(bookmark_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    obj = db.get(Bookmark, bookmark_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    db.delete(obj)
    db.commit()
    return JSONResponse(content={"detail": "deleted"})

# ---------------------------------------------------------------------------
# AI‑Powered Endpoints
# ---------------------------------------------------------------------------
class GenerateTagsRequest(BaseModel):
    url: str = Field(..., min_length=1)

class GenerateTagsResponse(BaseModel):
    generated_tags: List[str] = Field(default_factory=list)
    note: Optional[str] = None

@router.post("/ai/generate-tags", response_model=GenerateTagsResponse)
async def ai_generate_tags(req: GenerateTagsRequest):
    result = await generate_tags(req.url)
    return result

class SemanticSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)

class SemanticSearchResult(BaseModel):
    id: int
    title: str
    url: str
    similarity_score: float

class SemanticSearchResponse(BaseModel):
    results: List[SemanticSearchResult] = Field(default_factory=list)
    note: Optional[str] = None

@router.post("/ai/semantic-search", response_model=SemanticSearchResponse)
async def ai_semantic_search(req: SemanticSearchRequest):
    result = await semantic_search(req.query)
    return result