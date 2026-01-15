from sqlalchemy import Column, String, Boolean, DECIMAL, Date, DateTime, ForeignKey, Enum, Text, LargeBinary, Integer
from sqlalchemy.sql import func
from backend.app.core.database import Base
import uuid

# Helper to generate UUID string
def generate_uuid():
    return str(uuid.uuid4())

class Agent(Base):
    __tablename__ = "agent"

    agent_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100))
    mobile = Column(String(50))
    password_hash = Column(Text)
    created_at = Column(DateTime, default=func.now())
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(10), nullable=True) # Plain or Hashed (Plain for MVP)
    verification_code_expires_at = Column(DateTime, nullable=True)

class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(String(36), primary_key=True, default=generate_uuid)
    agent_id = Column(String(36), ForeignKey("agent.agent_id"))
    full_name = Column(LargeBinary(255)) # Encrypted
    mobile = Column(LargeBinary(255))    # Encrypted
    consent_flag = Column(Boolean)
    consent_time = Column(DateTime)
    created_at = Column(DateTime, default=func.now())

class Investment(Base):
    __tablename__ = "investment"

    investment_id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customer.customer_id"))
    scheme_type = Column(Enum('NSC','MIS','FD','KVP'))
    principal = Column(DECIMAL(12, 2))
    start_date = Column(Date)
    maturity_date = Column(Date)
    status = Column(Enum('ACTIVE','MATURED','FOLLOWUP','REINVESTED','CLOSED'))
    current_stage = Column(Enum('F10','F5','F3','F1','MT','P30'))

class FollowupLog(Base):
    __tablename__ = "followup_log"

    log_id = Column(String(36), primary_key=True, default=generate_uuid)
    investment_id = Column(String(36), ForeignKey("investment.investment_id"))
    stage = Column(Enum('F10','F5','F3','F1','MT','P30'))
    sent_on = Column(DateTime)
