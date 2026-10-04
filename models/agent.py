# from sqlalchemy import Column,Integer,String,Text,ForeignKey
# from sqlalchemy.orm import relationship
# from database.database import Base

# class Agent(Base):
#     __tablename__ = "agents"

#     id = Column(Integer,primary_key=True,index=True)

#     # Personal information
#     full_name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     phone = Column(String, unique=True, nullable=False)
#     address = Column(String, nullable=True)

#     gumba_id = Column(
#         Integer,
#         ForeignKey("gumbas.id"),
#         unique=True,
#         nullable=False
#     )

#     gumba = relationship(
#         "Gumba",
#         back_populates="agent"
#     )

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    # Existing user, if this agent came from a user application
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    # Personal information
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)

    # Identity verification
    identity_type = Column(String, nullable=False)
    identity_number = Column(String, unique=True, nullable=False)
    identity_document = Column(String, nullable=False)

    # Verification status
    verification_status = Column(
        String,
        nullable=False,
        default="approved"
    )

    # Gumba managed by agent
    gumba_id = Column(
        Integer,
        ForeignKey("gumbas.id"),
        unique=True,
        nullable=False
    )

    user = relationship("User")
    gumba = relationship(
        "Gumba",
        back_populates="agent"
    )