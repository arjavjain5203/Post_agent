
import asyncio
from backend.app.core.database import engine
from sqlalchemy import select
from backend.app.models.base import Agent

async def check_otp():
    async with engine.connect() as conn:
        result = await conn.execute(select(Agent.mobile, Agent.verification_code, Agent.is_verified).where(Agent.mobile == '9310082225'))
        agent = result.fetchone()
        if agent:
            print(f"Mobile: {agent.mobile}")
            print(f"Stored OTP: {agent.verification_code}")
            print(f"Verified: {agent.is_verified}")
        else:
            print("Agent not found")

if __name__ == "__main__":
    asyncio.run(check_otp())
