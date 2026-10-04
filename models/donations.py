from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
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
    user = relationship("User")
    gumba = relationship("Gumba")