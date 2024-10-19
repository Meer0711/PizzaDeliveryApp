from fastapi import APIRouter,Depends,HTTPException,status
from models import User,Order
from schemas import OrderModel
from sqlalchemy.orm import Session
from database import get_db
import oauth2
from typing import Optional


order_router=APIRouter(
    prefix='/orders',
    tags=['orders']
)


@order_router.get("/")
def hello():
    return {"message":"Hello World"}


@order_router.post("/orderPizza", status_code=status.HTTP_201_CREATED)
def place_an_order(order: OrderModel, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    # current_user already contains the authenticated user (fetched using the token)

    # Create a new order and associate it with the authenticated user
    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,
        user_id=current_user.id  # Link the order to the logged-in user
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Create the response dictionary
    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return response


@order_router.get("/allOrders")
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view all orders"
        )
    
    orders = db.query(Order).all()
    return (orders)


