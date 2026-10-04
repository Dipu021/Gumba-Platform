from pydantic import BaseModel


class CreateDonation(BaseModel):
    amount: float
    gumba_id: int