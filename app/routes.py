import random 
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import URL

router = APIRouter()

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

@router.post("/shorten")
def shorten_url(long_url: str, db: Session = Depends(get_db)):
    short_code = generate_short_code()
    new_url = URL(long_url = long_url, short_code = short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return {"short_code": short_code, "long_url": long_url}

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    
    url_entry.click_count += 1
    db.commit()
    return {"long_url": url_entry.long_url}

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
    
    


