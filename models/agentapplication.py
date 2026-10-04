from sqlalchemy import Column,Integer,String,Text,Float,ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class AgentApplication(Base):
    __tablename__ = "agent_applications"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    gumba_id = Column(
        Integer,
        ForeignKey("gumbas.id"),
        nullable=False
    )
    fullname = Column(String,nullable=False)
    phone = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    address = Column(String,nullable=True)
    identity_type = Column(String,nullable=False)
    identity_number = Column(String,nullable=False)
    identity_document = Column(String,nullable=False)
    status = Column(String,nullable=False,default="pending")
    rejection_reason = Column(Text,nullable=True)

    user = relationship("User")
    gumba = relationship("Gumba")