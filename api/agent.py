from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Form
from schemas.agent import CreateAgent,AgentResponse
from sqlalchemy.orm import Session
from database.database import get_db
from models.agent import Agent
from models.gumba import Gumba
from models.agentapplication import AgentApplication
from database.database import Base,engine
from services.get_current_user import get_current_user
import os
import uuid

router = APIRouter(prefix="/agent",tags=["Agent"])
# Create New Agent
@router.post("/admin")
async def create_agent(
    gumba_id:int=Form(...),
    full_name:str=Form(...),
    phone:str=Form(...),
    email:str=Form(...),
    address:str=Form(...),
    identity_type:str=Form(...),
    identity_number:str=Form(...),
    identity_document:UploadFile=File(...),
    db:Session=Depends(get_db)
    ):

    # Check For Gumba
    gumba = db.query(Gumba).filter(Gumba.id==gumba_id).first()
    if not gumba:
        raise HTTPException(
            status_code=404,
            detail="Gumba Not Found"
        )

    #Check Agent Exist
    existing_agent = db.query(Agent).filter(Agent.gumba_id==gumba_id).first()
    if existing_agent:
        raise HTTPException(
            status_code=400,
            detail="This Gumba Already have a agent"
        )
    # Validate Document
    allowed_types = {
        "image/jpeg",
        "image/png",
        "document/pdf"
        }
    if identity_document.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG,PNG or PDF Files are Allowed"
        )
    # saved Document
    os.makedirs(
        "uploads/identity",
        exist_ok=True
    )
    extension = os.path.splitext(
        identity_document.filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        "uploads","identity",filename
    )

    with open(file_path,"wb") as buffer:
        buffer.write(await identity_document.read())

    # Create Application
        application = Agent(
            user_id = None,
            gumba_id = gumba_id,
            full_name = full_name,
            phone = phone,
            email = email,
            address = address,
            identity_type = identity_type,
            identity_number = identity_number,
            identity_document = file_path,
            # status = "approved",
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        return{
        "message":"Agent Created Successfully Successfully",
        "application_id":application.id
    }


# Get Agents
@router.get("/agents",response_model=list[AgentResponse])
def get_agents(db:Session=Depends(get_db)):
    return db.query(Agent).all()

# Get Specific Agent

@router.get("/agents/{agent_id}",response_model=AgentResponse)
def get_agent(agent_id:int,db:Session=Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id==agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=404,
            detail="No Agent Found"
        )
    return agent

# user wants to be Agent
@router.post("/apply")
async def apply_as_agent(
    gumba_id:int=Form(...),
    full_name:str=Form(...),
    phone:str=Form(...),
    email:str=Form(...),
    address:str=Form(...),
    identity_type:str=Form(...),
    identity_number:str=Form(...),
    identity_document:UploadFile=File(...),
    db:Session=Depends(get_db),
    current_user = Depends(get_current_user)
):
    # check whether user already has an applicant
    existing_application = db.query(AgentApplication).filter(AgentApplication.user_id==current_user.id,AgentApplication.status=="pending").first()

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="You Already Have a Pending Application"
        )

    # Check For Gumba
    gumba = db.query(Gumba).filter(Gumba.id==gumba_id).first()

    if not gumba:
        raise HTTPException(
            status_code=404,
            detail="Gumba Not Found"
        )

    # Check Agent Exist
    existing_agent = db.query(Agent).filter(Agent.gumba_id==gumba_id).first()
    if existing_agent:
        raise HTTPException(
            status_code=400,
            detail="This Gumba Already have a agent"
        )

    # Validate Document
    allowed_types = {
        "image/jpeg",
        "image/png",
        "document/pdf"
    }

    if identity_document.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG,PNG or PDF Files are Allowed"
        )

    # saved Document
    os.makedirs(
        "uploads/identity",
        exist_ok=True
    )
    extension = os.path.splitext(
        identity_document.filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        "uploads","identity",filename
    )

    with open(file_path,"wb") as buffer:
        buffer.write(await identity_document.read())

    # Create Application
    application = AgentApplication(
        user_id = current_user.id,
        gumba_id = gumba_id,
        fullname = full_name,
        phone = phone,
        email = email,
        address = address,
        identity_type = identity_type,
        identity_number = identity_number,
        identity_document = file_path,
        status = "pending"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return{
        "message":"Agent Application Submitted Successfully",
        "application_id":application.id
    }


@router.patch("/applications/{application_id}/approve")
def approve_agent_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    application = (
        db.query(AgentApplication)
        .filter(AgentApplication.id == application_id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="Agent application not found")

    if application.status != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Application is already {application.status}",
        )

    existing_agent = (
        db.query(Agent)
        .filter(
            (Agent.gumba_id == application.gumba_id)
            | (Agent.user_id == application.user_id)
            | (Agent.email == application.email)
            | (Agent.phone == application.phone)
            | (Agent.identity_number == application.identity_number)
        )
        .first()
    )
    if existing_agent:
        raise HTTPException(
            status_code=409,
            detail="An agent already exists with this Gumba or applicant information",
        )

    agent = Agent(
        user_id=application.user_id,
        gumba_id=application.gumba_id,
        full_name=application.fullname,
        phone=application.phone,
        email=application.email,
        address=application.address,
        identity_type=application.identity_type,
        identity_number=application.identity_number,
        identity_document=application.identity_document,
        verification_status="approved",
    )

    application.status = "approved"
    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {
        "message": "Agent application approved successfully",
        "application_id": application.id,
        "agent_id": agent.id,
    }