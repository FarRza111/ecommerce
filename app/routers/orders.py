from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from .. import models, schemas, database
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME="your-email@example.com",
    MAIL_PASSWORD="your-password",
    MAIL_FROM="your-email@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

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
