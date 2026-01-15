import asyncio
from sqlalchemy import text
from db import engine

async def show_tables():
    async with engine.connect() as conn:
        result = await conn.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print("Tables in database:")
        for table in tables:
            print(f"- {table[0]}")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(show_tables())
