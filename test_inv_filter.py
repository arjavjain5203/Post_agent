
import asyncio
from backend.app.core.database import SessionLocal
from backend.app.services.customer_service import list_agent_customers
from backend.app.services.investment_service import list_investments
from sqlalchemy import select
from backend.app.models.base import Agent

async def test_filter():
    async with SessionLocal() as db:
        # Get Agent
        result = await db.execute(select(Agent).where(Agent.mobile == '9310082225'))
        agent = result.scalars().first()
        if not agent:
            print("Agent not found")
            return

        # Get Customers
        customers = await list_agent_customers(db, agent.agent_id)
        if not customers:
            print("No customers found")
            return
            
        target_customer = customers[0]
        print(f"Testing filter for Customer: {target_customer.full_name} ({target_customer.customer_id})")
        
        # Test Service Filter directly (as we updated service logic implicitly or endpoint relies on it)
        # Note: The endpoint logic for filtering was updated, but passed to list_investments(db, customer_id=...)
        # We need to verify that call works.
        
        invs = await list_investments(db, customer_id=target_customer.customer_id)
        print(f"Investments found: {len(invs)}")
        for inv in invs:
             print(f" - {inv.scheme_type}: {inv.principal}")

if __name__ == "__main__":
    asyncio.run(test_filter())
