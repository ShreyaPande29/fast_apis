from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_models import Cart,Order,CartItem,OrderItem,Pizza
from database import get_db

order_router = APIRouter()

@order_router.post("/orders/")
def place_order(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty.")

    total_amount = 0.0
    new_order = Order(user_id=user_id,total_amount=0.0)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    
    for item in cart.items:
        pizza = db.query(Pizza).filter(Pizza.id == item.item_id).first()
        if pizza:
            total_amount += pizza.price * item.quantity             
            order_item = OrderItem(order_id=new_order.id, item_id=item.item_id, quantity=item.quantity,item_price=pizza.price)
            db.add(order_item)

 
    new_order.total_amount = total_amount
    db.add(new_order)
    db.commit()
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()

    return {
        "message": "Order placed successfully!",
        "order_id": new_order.id,
        "total_amount": total_amount
    }