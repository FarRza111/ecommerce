from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from .. import models, schemas, database
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from .. import models, database
from fastapi.templating import Jinja2Templates

router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME="farrza111@gmail.com",
    MAIL_PASSWORD="Nizo2023",
    MAIL_FROM="farrza111@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


# Initialize Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/orders")
def view_orders(request: Request, db: Session = Depends(database.get_db)):
    # Fetch all orders (you can filter this by user in case of user-specific orders)
    orders = db.query(models.Order).all()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})


@router.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Send email notification in the background
    message = MessageSchema(
        subject="Order Confirmation",
        recipients=["user-email@example.com"],
        body="Thank you for your order!",
        subtype="plain"
    )
    background_tasks.add_task(FastMail(conf).send_message, message)

    return db_order
