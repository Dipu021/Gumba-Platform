from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateAgent(BaseModel):
    gumba_id: int
    full_name: str
    phone: str
    email: EmailStr
    address: Optional[str] = None
    identity_type: str
    identity_number: str


class AgentResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    address: Optional[str]

    identity_type: str
    identity_number: str
    identity_document: str
    verification_status: str

    gumba_id: int

    class Config:
        from_attributes = True
