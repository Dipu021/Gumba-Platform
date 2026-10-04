from fastapi import APIRouter,Depends,HTTPException
from schemas.gumba import CreateGumba,GumbaResponse
from sqlalchemy.orm import Session
from database.database import get_db
from models.gumba import Gumba
from models.agent import Agent
from models.user import User
from models.donations import Donation
from database.database import Base,engine
from security.oauth2 import verify_token
from schemas.donations import CreateDonation
from services.email import send_mail

# app = FastAPI()
router = APIRouter(prefix="/donations",tags=["Donations"])


@router.post("/donations")
async def create_donatinos(data:CreateDonation,username:str=Depends(verify_token),db:Session=Depends(get_db)):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )

    gumba = db.query(Gumba).filter(Gumba.id == data.gumba_id).first()
    if not gumba:
        raise HTTPException(
            status_code=404,
            detail="Gumba not found"
        )

    new_donation = Donation(
        amount = data.amount,
        user_id = user.id,
        gumba_id=gumba.id
    )
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    await send_mail([user.email])

    return {
        "message":f"{data.amount} Donated Successfully to {gumba.name}",
        "user_id":user.id
    }