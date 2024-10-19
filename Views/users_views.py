from fastapi import Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
from models.models import (CustomerCreate, OrderResponse,
UserUpdate,
UserResponse)
from db_models import User,Role,Order
from database import get_db
from utils.utils_auth import hash_password
from typing import List

user_router = APIRouter()

@user_router.post("/register", response_model=dict)
def register_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == customer.username).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new customer with the 'customer' role
    hashed_password = hash_password(customer.password)
    new_customer = User(
        name=customer.name, 
        username=customer.username, 
        password=hashed_password, 
        mobile=customer.mobile,
        address =customer.address,
        role=Role.customer
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {"message": "Customer registered successfully"}

# API to edit user details
@user_router.put("/users/{user_id}", response_model=UserResponse)
def edit_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only the fields that are provided
    if user_update.name:
        user.name = user_update.name    
    if user_update.mobile:
        user.mobile = user_update.mobile
    if user_update.address:
        user.address = user_update.address

    db.commit()
    db.refresh(user)
    return user

@user_router.get("/users/{user_id}/orders/")
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    # Query to get orders for the user
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user.")

    # Prepare the response to include order items
    response = []
    for order in orders:
        
        order_details = {
            "order_id": order.id,
            "total_amount": order.total_amount,    
            "created_at":order.created_at,        
            "order_items": []
        }


        for item in order.order_items:
            order_details["order_items"].append({
                "item_id": item.item_id,
                "quantity": item.quantity,
                "price":item.item_price
            })
        response.append(order_details)

    return response
