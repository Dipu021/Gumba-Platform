from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional


class Address(BaseModel):
    province: str
    district: str
    municipality: str
    ward: int
    tole: str


class Location(BaseModel):
    latitude: float
    longitude: float


class Contact(BaseModel):
    phone: str
    email: EmailStr


class CreateGumba(BaseModel):
    name: str
    description: str
    registration_number: str

    address: Address
    location: Location
    contact: Contact

    established_year: Optional[int] = None
    status: str = "active"


class GumbaResponse(BaseModel):
    id: int
    name: str
    description: str
    registration_number: str

    address: Address
    location: Location
    contact: Contact

    established_year: Optional[int] = None
    status: str

    class Config:
        from_attributes = True
