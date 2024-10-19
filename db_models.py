from sqlalchemy import Column, Integer, String, Enum,Float,ForeignKey,DateTime,Boolean
from database import Base
import enum
from sqlalchemy.orm import relationship
from datetime import datetime

class Role(enum.Enum):
    admin = "admin"
    delivery_partner = "delivery_partner"
    customer = "customer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mobile = Column(String(10),index=True)
    address = Column(String)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(Role), default=Role.customer)

    cart = relationship("Cart", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")


class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    pizza_type = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)


class PartnerStatus(enum.Enum):
    active = "active"
    inactive = "inactive"

class DeliveryPartner(Base):
    __tablename__ = "delivery_partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    status = Column(Enum(PartnerStatus), default=PartnerStatus.active)



class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    item_id = Column(Integer, nullable=False)  # You would replace this with the actual item model's ID
    quantity = Column(Integer, default=1)

    cart = relationship("Cart", back_populates="items")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")  

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    item_id = Column(Integer, nullable=False)  
    quantity = Column(Integer, default=1)
    item_price = Column(Float)

    order = relationship("Order", back_populates="order_items")

