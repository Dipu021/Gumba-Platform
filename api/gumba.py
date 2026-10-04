from fastapi import APIRouter,Depends,HTTPException
from schemas.gumba import CreateGumba,GumbaResponse
from sqlalchemy.orm import Session
from database.database import get_db
from models.gumba import Gumba
from models.agent import Agent
from database.database import Base,engine

router = APIRouter(prefix="/gumba",tags=["Gumbas"])

@router.post("/gumbas")
def create_gumba(data:CreateGumba,db:Session=Depends(get_db)):
    # Create New Gumba
    new_gumba = Gumba(
                name = data.name,
                description = data.description,
                registration_number = data.registration_number,
                province = data.address.province,
                district = data.address.district,
                municipality = data.address.municipality,
                ward = data.address.ward,
                tole = data.address.tole,
                latitude = data.location.latitude,
                longitude = data.location.longitude,
                phone = data.contact.phone,
                email = data.contact.email,
                established_year = data.established_year,
                status = data.status

        )
    db.add(new_gumba)
    db.commit()
    db.refresh(new_gumba)
    return {
        "message": "Gumba Created successfully",
        "gumba_id":new_gumba.id
    }

def format_gumba(gumba: Gumba):
    return {
        "id": gumba.id,
        "name": gumba.name,
        "description": gumba.description,
        "registration_number": gumba.registration_number,
        "address": {
            "province": gumba.province,
            "district": gumba.district,
            "municipality": gumba.municipality,
            "ward": gumba.ward,
            "tole": gumba.tole,
        },
        "location": {
            "latitude": gumba.latitude,
            "longitude": gumba.longitude,
        },
        "contact": {
            "phone": gumba.phone,
            "email": gumba.email,
        },
        "established_year": gumba.established_year,
        "status": gumba.status,
    }


@router.get("/gumbas", response_model=list[GumbaResponse])
def get_gumbas(db: Session = Depends(get_db)):
    gumbas = db.query(Gumba).all()
    return [format_gumba(gumba) for gumba in gumbas]

@router.get("/gumbas/{gumba_id}", response_model=GumbaResponse)
def get_gumba(gumba_id: int, db: Session = Depends(get_db)):
    gumba = db.query(Gumba).filter(Gumba.id == gumba_id).first()
    if not gumba:
        raise HTTPException(status_code=404, detail="No Gumba Found")

    return format_gumba(gumba)