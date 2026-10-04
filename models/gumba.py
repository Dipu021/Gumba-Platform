from sqlalchemy import Column,Integer,String,Text,Float,ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Gumba(Base):
    __tablename__ = "gumbas"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,unique=True,nullable=False)
    description = Column(Text,nullable=False)
    registration_number = Column(String,nullable=False,unique=True)

    # Address
    province = Column(String, nullable=False)
    district = Column(String, nullable=False)
    municipality = Column(String, nullable=False)
    ward = Column(Integer, nullable=False)
    tole = Column(String, nullable=False)

    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # Other information
    established_year = Column(Integer, nullable=True)
    status = Column(String, nullable=False, default="active")

    agent = relationship(
        "Agent",
        back_populates="gumba",
        uselist=False
    )