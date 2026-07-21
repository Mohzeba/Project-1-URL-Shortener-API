import random 
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import URL
from typing import Optional
import redis
import os

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

router = APIRouter()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

@router.post("/shorten")
def shorten_url(long_url: str, custom_code: str = None, db: Session = Depends(get_db)):
    short_code = custom_code if custom_code else generate_short_code()

    existing = db.query(URL).filter(URL.short_code == short_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Short code already exists")

    new_url = URL(long_url = long_url, short_code = short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return {"short_code": short_code, "long_url": long_url}

@router.get("/urls")
def list_urls(db: Session = Depends(get_db)):
    return db.query(URL).all()

@router.get("/{short_code}/stats")
def get_stats(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    return{
        "short_code": url_entry.short_code,
        "long_url": url_entry.long_url,
        "click_count": url_entry.click_count,
        "created_at": url_entry.created_at
    }

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    cached_url = redis_client.get(short_code)
    if cached_url:
        db.query(URL).filter(URL.short_code == short_code).update(
            {URL.click_count: URL.click_count + 1}
        )
        db.commit
        return {"long_url": cached_url, "source": "cache"}
    
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail= "URL not found")
    
    url_entry.click_count += 1
    db.commit()

    redis_client.set(short_code, url_entry.long_url, ex=3600)

    return {"long_url": url_entry.long_url, "source": "database" }

@router.delete("/{short_code}")
def delete_url(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url_entry)
    db.commit()
    return {"detail": f"{short_code} deleted"}