from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api import deps
from backend.app.core.database import get_db
from backend.app.models.base import Agent
from backend.app.schemas.customer import CustomerCreate, CustomerResponse
from backend.app.services import customer_service

router = APIRouter()

@router.post("/", response_model=CustomerResponse)
async def create_customer(
    customer_in: CustomerCreate,
    current_agent: Agent = Depends(deps.get_current_agent),
    db: AsyncSession = Depends(get_db)
):
    return await customer_service.create_new_customer(db, customer_in, current_agent.agent_id)

@router.get("/", response_model=List[CustomerResponse])
async def read_customers(
    current_agent: Agent = Depends(deps.get_current_agent),
    db: AsyncSession = Depends(get_db)
):
    return await customer_service.list_agent_customers(db, current_agent.agent_id)

@router.get("/{customer_id}", response_model=CustomerResponse)
async def read_customer(
    customer_id: str,
    current_agent: Agent = Depends(deps.get_current_agent),
    db: AsyncSession = Depends(get_db)
):
    customer = await customer_service.get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.agent_id != current_agent.agent_id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return customer
