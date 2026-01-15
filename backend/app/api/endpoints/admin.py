from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import timedelta

from backend.app.core.database import get_db
from backend.app.core.config import settings
from backend.app.core.security import create_access_token
from backend.app.api.deps import get_current_admin
from backend.app.schemas.admin import AdminLogin, SystemStats
from backend.app.schemas.auth import Token
# ... other imports ...

from backend.app.models.base import Agent, Customer, Investment, FollowupLog

router = APIRouter()

@router.post("/login", response_model=None)
async def admin_login(login_data: AdminLogin, response: Response):
    if not settings.ADMIN_SECRET:
        raise HTTPException(status_code=500, detail="Admin secret not configured")
    
    if login_data.secret_key != settings.ADMIN_SECRET:
         raise HTTPException(status_code=401, detail="Invalid admin secret")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject="admin", expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False,
    )
    
    return {"message": "Admin Login successful"}

@router.get("/stats", response_model=SystemStats, dependencies=[Depends(get_current_admin)])
async def get_system_stats(db: AsyncSession = Depends(get_db)):
    # Count Agents
    agent_count = await db.scalar(select(func.count(Agent.agent_id)))
    
    # Count Customers
    customer_count = await db.scalar(select(func.count(Customer.customer_id)))
    
    # Count Investments
    investment_count = await db.scalar(select(func.count(Investment.investment_id)))
    
    # Total Investment Value
    inv_value_result = await db.execute(select(func.sum(Investment.principal)))
    total_value = inv_value_result.scalar() or 0.0
    
    # Pending Followups (All Stages)
    # Actually, let's count Active Investments that are NOT matured/closed as well
    pending_followups = await db.scalar(select(func.count(FollowupLog.log_id))) # This counts logs sent.
    
    # Maybe "Pending Followups" means Active Investments currently in a stage?
    # Or just return count of active investments.
    # Let's count "Active" investments for now as a proxy or just count total logs.
    # To keep it simple and match the schema:
    pending_followups_count = await db.scalar(select(func.count(Investment.investment_id)).where(Investment.status == 'FOLLOWUP'))

    return SystemStats(
        total_agents=agent_count or 0,
        total_customers=customer_count or 0,
        total_investments=investment_count or 0,
        total_investment_value=float(total_value),
        pending_followups=pending_followups_count or 0
    )
