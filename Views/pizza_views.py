from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.models import (PizzaCreate,
PizzaEdit,
PizzaResponse)
from db_models import Pizza
from database import get_db
from utils.utils_auth import is_admin,oauth2_scheme

pizza_router = APIRouter()

# API to add a new pizza
@pizza_router.post("/pizzas/", response_model=PizzaResponse)
def add_pizza(pizza: PizzaCreate, token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    is_admin(token)

    existing_pizza = db.query(Pizza).filter(Pizza.name == pizza.name).first()
    if existing_pizza:
        raise HTTPException(status_code=400, detail="Pizza already exists")

    new_pizza = Pizza(**pizza.dict())
    db.add(new_pizza)
    db.commit()
    db.refresh(new_pizza)
    return new_pizza

# API to list all pizzas
@pizza_router.get("/pizzas/", response_model=List[PizzaResponse])
def list_pizzas(db: Session = Depends(get_db)):
    pizzas = db.query(Pizza).all()
    return pizzas

# API to retrieve a pizza by ID
@pizza_router.get("/pizzas/{pizza_id}", response_model=PizzaResponse)
def retrieve_pizza(pizza_id: int, db: Session = Depends(get_db)):

    pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    return pizza

# API to edit a pizza's details
@pizza_router.put("/pizzas/{pizza_id}", response_model=PizzaResponse)
def edit_pizza(pizza_id: int, updated_pizza: PizzaEdit,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    is_admin(token)
    pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    pizza.name = updated_pizza.name
    pizza.description = updated_pizza.description
    pizza.price = updated_pizza.price
    pizza.pizza_type = updated_pizza.pizza_type
    pizza.is_avaliable = updated_pizza.is_available

    db.commit()
    db.refresh(pizza)
    return pizza

# API to delete a pizza by ID
@pizza_router.delete("/pizzas/{pizza_id}")
def delete_pizza(pizza_id: int,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    is_admin(token)
    pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    db.delete(pizza)
    db.commit()
    return {"message": "Pizza deleted successfully"}
