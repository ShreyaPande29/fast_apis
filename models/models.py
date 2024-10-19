from pydantic import BaseModel,Field
from typing import List,Optional
from enum import Enum

# User classes
class CustomerCreate(BaseModel):
    name: str
    username: str
    password: str
    mobile:  str
    address: str

class UserUpdate(BaseModel):
    name: Optional[str]    = Field(None, description="User's name")
    mobile: Optional[str]
    address : Optional[str]

class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    mobile: Optional[str]
    address : Optional[str]

    class Config:
        orm_mode = True

#Pizza Classes
class PizzaCreate(BaseModel):
    name: str
    description: str
    price: float
    pizza_type: str

class PizzaEdit(BaseModel):
    name: str
    description: str
    price: float
    pizza_type: str
    is_available: Optional[bool]

class PizzaResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    pizza_type: str

    class Config:
        orm_mode = True


#Delivery partner
class PartnerStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class DeliveryPartnerCreate(BaseModel):
    name: str
    phone_number: str
    status: Optional[PartnerStatus] = PartnerStatus.active

class DeliveryPartnerResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    status: PartnerStatus

    class Config:
        orm_mode = True






# Pydantic model for placing an order
class OrderCreate(BaseModel):
    user_id: int


# Pydantic model for Order response
class OrderResponse(BaseModel):
    id: int
    user_id: int
    cart_id: int
    total_amount: float
    created_at: str

    class Config:
        orm_mode = True


#Cart
class CartItemCreate(BaseModel):
    item_id: int
    quantity: int

class CartItemsCreate(BaseModel):
    items: List[CartItemCreate]

class CartItemResponse(BaseModel):
    id: int
    item_id: int
    quantity: int

    class Config:
        orm_mode = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]

    class Config:
        orm_mode = True
