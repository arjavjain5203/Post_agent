from pydantic import BaseModel

class AdminLogin(BaseModel):
    secret_key: str

class SystemStats(BaseModel):
    total_agents: int
    total_customers: int
    total_investments: int
    total_investment_value: float
    pending_followups: int
