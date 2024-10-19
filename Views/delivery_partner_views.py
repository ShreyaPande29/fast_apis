from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from typing import List
from models.models import *
from db_models import *
from database import get_db
from utils.utils_auth import is_admin,oauth2_scheme

dp_router = APIRouter()

@dp_router.post("/delivery-partners/", response_model=DeliveryPartnerResponse)
def add_delivery_partner(partner: DeliveryPartnerCreate,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Check if the phone number is already registered
    is_admin(token)
    existing_partner = db.query(DeliveryPartner).filter(DeliveryPartner.phone_number == partner.phone_number).first()
    if existing_partner:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    # Create a new delivery partner
    new_partner = DeliveryPartner(
        name=partner.name,
        phone_number=partner.phone_number,
        status=partner.status
    )
    db.add(new_partner)
    db.commit()
    db.refresh(new_partner)

    return new_partner

@dp_router.get("/delivery-partners/", response_model=List[DeliveryPartnerResponse])
def list_delivery_partners(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    is_admin(token)
    partners = db.query(DeliveryPartner).all()
    return partners

@dp_router.get("/delivery-partners/{partner_id}", response_model=DeliveryPartnerResponse)
def retrieve_delivery_partner(partner_id: int,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    is_admin(token)
    partner = db.query(DeliveryPartner).filter(DeliveryPartner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Delivery partner not found")
    return partner

@dp_router.put("/delivery-partners/{partner_id}", response_model=DeliveryPartnerResponse)
def edit_delivery_partner(
    partner_id: int, updated_partner: DeliveryPartnerCreate,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    is_admin(token)
    partner = db.query(DeliveryPartner).filter(DeliveryPartner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Delivery partner not found")

    # Update partner's details
    partner.name = updated_partner.name
    partner.phone_number = updated_partner.phone_number
    partner.status = updated_partner.status

    db.commit()
    db.refresh(partner)
    return partner

# API to delete a delivery partner
@dp_router.delete("/delivery-partners/{partner_id}")
def delete_delivery_partner(partner_id: int,token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    is_admin(token)
    partner = db.query(DeliveryPartner).filter(DeliveryPartner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Delivery partner not found")

    db.delete(partner)
    db.commit()
    return {"message": "Delivery partner deleted successfully"}
