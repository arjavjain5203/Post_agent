from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from backend.app.core.database import get_db
from backend.app.api.deps import get_current_agent
from backend.app.schemas.admin import SystemStats # Reusing schema as structure is same
from backend.app.models.base import Agent, Customer, Investment, FollowupLog

router = APIRouter()

@router.get("/stats", response_model=SystemStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_agent: Agent = Depends(get_current_agent)
):
    # Filter by Current Agent
    
    # Count Customers
    customer_count = await db.scalar(
        select(func.count(Customer.customer_id))
        .where(Customer.agent_id == current_agent.agent_id)
    )
    
    # Count Investments (joined via Customer)
    investment_count = await db.scalar(
        select(func.count(Investment.investment_id))
        .join(Customer, Investment.customer_id == Customer.customer_id)
        .where(Customer.agent_id == current_agent.agent_id)
    )
    
    # Total Investment Value
    inv_value_result = await db.execute(
        select(func.sum(Investment.principal))
        .join(Customer, Investment.customer_id == Customer.customer_id)
        .where(Customer.agent_id == current_agent.agent_id)
    )
    total_value = inv_value_result.scalar() or 0.0
    
    # Pending Followups (Active Investments in FOLLOWUP status)
    pending_followups_count = await db.scalar(
        select(func.count(Investment.investment_id))
        .join(Customer, Investment.customer_id == Customer.customer_id)
        .where(Customer.agent_id == current_agent.agent_id)
        .where(Investment.status == 'FOLLOWUP')
    )

    return SystemStats(
        total_agents=1, # Irrelevant for agent view
        total_customers=customer_count or 0,
        total_investments=investment_count or 0,
        total_investment_value=float(total_value),
        pending_followups=pending_followups_count or 0
    )
