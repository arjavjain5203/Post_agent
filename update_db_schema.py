import asyncio
from sqlalchemy import text
from backend.app.core.database import engine

async def update_schema():
    async with engine.begin() as conn:
        print("Adding created_at column to customer table...")
        try:
            # Check if column exists first (prevent error if re-ran)
            # Actually easier to just try add and ignore error or check info schema.
            # MySQL syntax
            await conn.execute(text("ALTER TABLE customer ADD COLUMN created_at DATETIME DEFAULT NOW();"))
            print("Column added successfully.")
        except Exception as e:
            print(f"Error (column might already exist): {e}")

if __name__ == "__main__":
    asyncio.run(update_schema())
