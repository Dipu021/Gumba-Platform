from pydantic import BaseModel,EmailStr
from typing import Optional

class AgentApplication(BaseModel):
    gumba_id:int
    full_name:str
    phone:str
    email:EmailStr
    address:Optional[str]=None
    identity_type :str
    identity_number:str