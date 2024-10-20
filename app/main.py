from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .routers import products, users, orders, categories
from .database import engine, Base

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Static files for CSS and images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(categories.router)

@app.get("/")
async def home(request: Request, db: Session = Depends(database.get_db)):
    categories = db.query(models.Product.category).distinct().all()
    products = db.query(models.Product).all()
    return templates.TemplateResponse("index.html", {"request": request, "categories": categories, "products": products})
