import asyncio
from sqlalchemy import text
from backend.app.core.database import engine

async def update_schema():
    async with engine.begin() as conn:
        print("Adding security columns to agent table...")
        try:
            await conn.execute(text("ALTER TABLE agent ADD COLUMN failed_login_attempts INT DEFAULT 0;"))
            print("Added failed_login_attempts.")
        except Exception as e:
            print(f"Error adding failed_login_attempts: {e}")
            
        try:
            await conn.execute(text("ALTER TABLE agent ADD COLUMN locked_until DATETIME NULL;"))
            print("Added locked_until.")
        except Exception as e:
            print(f"Error adding locked_until: {e}")

if __name__ == "__main__":
    asyncio.run(update_schema())
