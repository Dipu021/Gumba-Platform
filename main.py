from fastapi import FastAPI

from database.database import Base, engine

from models.user import User
from models.gumba import Gumba
from models.agent import Agent
from models.donations import Donation
from api.gumba import router as gumba_router
from api.donations import router as donation_router
from api.auth import router as auth_router
from api.agent import router as agent_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(gumba_router)
app.include_router(auth_router)
app.include_router(agent_router)
app.include_router(donation_router)