from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    agent_id: Optional[str] = None

class AgentCreate(BaseModel):
    name: str
    mobile: str
    password: str

class AgentLogin(BaseModel):
    mobile: str
    password: str

class VerifyOTP(BaseModel):
    mobile: str
    otp: str

class ResendOTP(BaseModel):
    mobile: str

class AgentResponse(BaseModel):
    agent_id: str
    name: str
    mobile: str
    
    class Config:
        from_attributes = True
