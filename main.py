from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine
from typing import List
from models.models import *
from db_models import *
from database import Base,get_db
from Views.users_views import user_router
from Views.pizza_views import pizza_router
from Views.delivery_partner_views import dp_router
from Views.cart_views import cart_router
from Views.order_views import order_router
from fastapi.security import OAuth2PasswordRequestForm
from utils.utils_auth import verify_password, create_access_token
from datetime import datetime, timedelta
# Create tables in the database
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first() 
    
    hased_pass = user.password
    user_role = user.role.value

    
    if not user or not verify_password(form_data.password,hased_pass ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=30)
    
    access_token = create_access_token(
        data={"sub": form_data.username,"role":user_role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}





app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(pizza_router, prefix="/pizza", tags=["Pizzas"])
app.include_router(dp_router, prefix="/dps", tags=["Deliver Partners"])
app.include_router(cart_router, prefix="/cart", tags=["Cart"])
app.include_router(order_router, prefix="/place-order", tags=["Order"])