from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    full_name: str
    mobile: str
    consent_flag: bool = False

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: str
    agent_id: str
    consent_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
