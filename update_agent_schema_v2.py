import asyncio
from sqlalchemy import text
from backend.app.core.database import engine

async def update_schema():
    print("Updating schema to add verification columns...")
    async with engine.begin() as conn:
        try:
            # 1. Add is_verified
            await conn.execute(text("ALTER TABLE agent ADD COLUMN is_verified BOOLEAN DEFAULT FALSE;"))
            print("Added is_verified column.")
        except Exception as e:
            print(f"Skipping is_verified: {e}")

        try:
            # 2. Add verification_code
            await conn.execute(text("ALTER TABLE agent ADD COLUMN verification_code VARCHAR(10);"))
            print("Added verification_code column.")
        except Exception as e:
            print(f"Skipping verification_code: {e}")

        try:
            # 3. Add verification_code_expires_at
            await conn.execute(text("ALTER TABLE agent ADD COLUMN verification_code_expires_at DATETIME;"))
            print("Added verification_code_expires_at column.")
        except Exception as e:
            print(f"Skipping verification_code_expires_at: {e}")
            
    print("Schema update complete.")

if __name__ == "__main__":
    asyncio.run(update_schema())
