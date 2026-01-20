from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api import deps
from backend.app.core.database import get_db
from backend.app.models.base import Agent
from backend.app.schemas.investment import InvestmentCreate, InvestmentResponse
from backend.app.services import investment_service, customer_service

router = APIRouter()

@router.post("/", response_model=InvestmentResponse)
async def create_investment(
    investment_in: InvestmentCreate,
    current_agent: Agent = Depends(deps.get_current_agent),
    db: AsyncSession = Depends(get_db)
):
    # Verify customer belongs to agent
    customer = await customer_service.get_customer_by_id(db, investment_in.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.agent_id != current_agent.agent_id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
        
    return await investment_service.create_investment(db, investment_in)

@router.get("/", response_model=List[InvestmentResponse])
async def read_investments(
    customer_id: str = None,
    current_agent: Agent = Depends(deps.get_current_agent),
    db: AsyncSession = Depends(get_db)
):
    # If customer_id provided, fetch only for that customer (after verifying ownership)
    if customer_id:
        customer = await customer_service.get_customer_by_id(db, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        if customer.agent_id != current_agent.agent_id:
            raise HTTPException(status_code=400, detail="Not enough permissions")
            
        return await investment_service.list_investments(db, customer_id=customer_id)

    # Get all customers of agent
    customers = await customer_service.list_agent_customers(db, current_agent.agent_id)
    customer_ids = [c.customer_id for c in customers]
    
    # Now get investments for these customers
    all_investments = []
    for cid in customer_ids:
        invs = await investment_service.list_investments(db, customer_id=cid)
        all_investments.extend(invs)
        
    return all_investments
