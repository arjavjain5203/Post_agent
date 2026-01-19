
import asyncio
from backend.app.core.database import engine
from sqlalchemy import select
from backend.app.models.base import Agent

async def list_agents():
    async with engine.connect() as conn:
        result = await conn.execute(select(Agent.name, Agent.mobile, Agent.is_verified))
        agents = result.fetchall()
        print(f"Total Agents: {len(agents)}")
        for a in agents:
            print(f"Name: {a.name}, Mobile: {a.mobile}, Verified: {a.is_verified}")

if __name__ == "__main__":
    asyncio.run(list_agents())
