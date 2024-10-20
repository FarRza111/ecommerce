from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter()

# Directory to store uploaded images
UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists



@router.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products/", response_model=List[schemas.Product])
def get_products(
    category: str = None, 
    search: str = None, 
    min_price: float = None, 
    max_price: float = None, 
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Product)
    
    if category:
        query = query.filter(models.Product.category == category)
    
    if search:
        query = query.filter(models.Product.name.contains(search))
    
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    
    return query.all()



from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
import shutil
from .. import models, schemas, database



@router.post("/products/", response_model=schemas.Product)
def create_product(
    name: str,
    description: str,
    price: float,
    category: str,
    file: UploadFile = File(...),  # File upload
    db: Session = Depends(database.get_db)
):
    # Generate a file path for the uploaded image
    file_path = UPLOAD_DIR / file.filename
    
    # Save the uploaded image to the server
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create the product with the image URL
    image_url = f"/static/uploads/{file.filename}"
    
    new_product = models.Product(
        name=name,
        description=description,
        price=price,
        category=category,
        image_url=image_url
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product



