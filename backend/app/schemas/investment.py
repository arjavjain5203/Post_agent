from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class SchemeType(str, Enum):
    NSC = 'NSC'
    MIS = 'MIS'
    FD = 'FD'
    KVP = 'KVP'

class InvestmentStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    MATURED = 'MATURED'
    FOLLOWUP = 'FOLLOWUP'
    REINVESTED = 'REINVESTED'
    CLOSED = 'CLOSED'

class StageEnum(str, Enum):
    F10 = 'F10'
    F5 = 'F5'
    F3 = 'F3'
    F1 = 'F1'
    MT = 'MT'
    P30 = 'P30'

class InvestmentBase(BaseModel):
    scheme_type: SchemeType
    principal: float
    start_date: date
    maturity_date: date
    status: InvestmentStatus = InvestmentStatus.ACTIVE
    current_stage: Optional[StageEnum] = None

class InvestmentCreate(InvestmentBase):
    customer_id: str

class InvestmentResponse(InvestmentBase):
    investment_id: str
    customer_id: str

    class Config:
        from_attributes = True
