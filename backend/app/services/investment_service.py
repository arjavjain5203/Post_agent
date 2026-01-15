from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from backend.app.models.base import Investment
from backend.app.schemas.investment import InvestmentCreate

async def create_investment(db: AsyncSession, investment_in: InvestmentCreate) -> Investment:
    db_investment = Investment(
        customer_id=investment_in.customer_id,
        scheme_type=investment_in.scheme_type,
        principal=investment_in.principal,
        start_date=investment_in.start_date,
        maturity_date=investment_in.maturity_date,
        status=investment_in.status,
        current_stage=investment_in.current_stage
    )
    db.add(db_investment)
    await db.commit()
    await db.refresh(db_investment)
    return db_investment

async def list_investments(db: AsyncSession, customer_id: str = None) -> List[Investment]:
    if customer_id:
        stmt = select(Investment).where(Investment.customer_id == customer_id)
    else:
        # TODO: Filter by agent ownership via join? 
        # For now, allow listing all (API layer ensures permissions usually)
        stmt = select(Investment)
        
    result = await db.execute(stmt)
    return result.scalars().all()
