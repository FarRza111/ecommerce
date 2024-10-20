from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter()

@router.get("/categories/")
def get_categories(db: Session = Depends(database.get_db)):
    categories = db.query(models.Product.category).distinct().all()
    return [category[0] for category in categories]
