
import asyncio
from datetime import date, timedelta
from backend.app.core.database import SessionLocal
from backend.app.models.base import Agent, Customer, Investment
from backend.app.services.followup_engine import check_daily_followups
from backend.app.schemas.investment import InvestmentStatus, SchemeType
from backend.app.core.security import encrypt_field
import uuid

async def setup_test_data():
    async with SessionLocal() as db:
        # 1. Find or Create Agent (Arjav)
        # We know Arjav exists from previous steps (9310082225)
        from sqlalchemy import select
        result = await db.execute(select(Agent).where(Agent.mobile == '9310082225'))
        agent = result.scalars().first()
        if not agent:
            print("Agent '9310082225' not found. Creating...")
            agent = Agent(
                name="Arjav Jain",
                mobile="9310082225",
                is_verified=True
            )
            db.add(agent)
            await db.commit()
            await db.refresh(agent)
            
        print(f"Using Agent: {agent.name} ({agent.mobile})")

        # 2. Create Customer
        customer = Customer(
            customer_id=str(uuid.uuid4()),
            agent_id=agent.agent_id,
            full_name=encrypt_field("Test Customer").encode('utf-8'),
            mobile=encrypt_field("9998887776").encode('utf-8'),
            consent_flag=True
        )
        db.add(customer)
        
        # 3. Create Investment with Maturity 10 days from now (F10 trigger)
        inv_f10 = Investment(
            investment_id=str(uuid.uuid4()),
            customer_id=customer.customer_id,
            scheme_type='FD',
            principal=50000.00,
            start_date=date.today() - timedelta(days=365),
            maturity_date=date.today() + timedelta(days=10), # 10 days from now
            status='ACTIVE'
        )
        db.add(inv_f10)
        await db.commit()
        print("Created Test Investment (Maturity in 10 days)")

async def run_trigger():
    print("--- Triggering Follow-up Scan ---")
    await check_daily_followups()
    print("--- Scan Complete ---")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_test_data())
    loop.run_until_complete(run_trigger())
