from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.models import CartItemResponse,CartItemsCreate,CartResponse
from db_models import User,Cart,CartItem
from database import get_db

cart_router = APIRouter()

@cart_router.post("/carts/{user_id}/items/", response_model=List[CartItemResponse])
def add_multiple_items_to_cart(user_id: int, cart_items: CartItemsCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    added_items = []
    for item in cart_items.items:
        cart_item = CartItem(cart_id=cart.id, item_id=item.item_id, quantity=item.quantity)
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        added_items.append(cart_item)
    
    return added_items

# API to list cart items
@cart_router.get("/carts/{user_id}/", response_model=CartResponse)
def list_cart_items(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    return cart


@cart_router.delete("/carts/{user_id}/items/{item_id}", response_model=dict)
def remove_item_from_cart(user_id: int, item_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    
    return {"message": "Item removed from cart", "item_id": item_id}

@cart_router.put("/carts/{user_id}/items/{item_id}", response_model=CartItemResponse)
def update_cart_item(user_id: int, item_id: int, quantity: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)

    return cart_item

