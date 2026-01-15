
import asyncio
from backend.app.core.database import engine, Base
# Import all models to ensure they are registered with Base.metadata
from backend.app.models.base import Agent, Customer, Investment, FollowupLog

async def reset_database():
    print("Resetting database...")
    async with engine.begin() as conn:
        print("Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
    print("Database reset complete.")

if __name__ == "__main__":
    asyncio.run(reset_database())
