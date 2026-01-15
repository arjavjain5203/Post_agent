import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

import sys
import ssl
# Construct database URL
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_ssl_enabled = os.getenv('DB_SSL', 'false').lower() == 'true'

if not all([db_user, db_password, db_host, db_port, db_name]):
    print("Warning: One or more database environment variables are missing.")

# Connect using aiomysql
# Note: We remove ?ssl=true from the URL and pass it via connect_args
DATABASE_URL = f"mysql+aiomysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

connect_args = {}
if db_ssl_enabled:
    # Create a default SSL context. 
    # For many cloud DBs (like Aiven), a default context works if public certs are used.
    # We set check_hostname=False and verify_mode=CERT_NONE for maximum compatibility during dev
    # unless specific cert paths are provided. 
    # Aiven usually requires CA certs for strict verification, but often allows connection 
    # with just SSL encryption if we don't strictly verify the CA.
    # Let's try creates_default_context first.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connect_args['ssl'] = ctx

# Define engine at module level so it can be imported
engine = create_async_engine(
    DATABASE_URL,
    pool_recycle=1800,
    pool_pre_ping=True,
    connect_args=connect_args
)

async def create_tables():
    async with engine.begin() as conn:
        # Create agent table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS agent (
                agent_id CHAR(36) PRIMARY KEY,
                name VARCHAR(100),
                mobile VARCHAR(50),
                password_hash TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """))

        # Create customer table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS customer (
                customer_id CHAR(36) PRIMARY KEY,
                agent_id CHAR(36),
                full_name VARBINARY(255),
                mobile VARBINARY(255),
                consent_flag BOOLEAN,
                consent_time DATETIME,
                FOREIGN KEY(agent_id) REFERENCES agent(agent_id)
            );
        """))

        # Create investment table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS investment (
              investment_id CHAR(36) PRIMARY KEY,
              customer_id CHAR(36),
              scheme_type ENUM('NSC','MIS','FD','KVP'),
              principal DECIMAL(12,2),
              start_date DATE,
              maturity_date DATE,
              status ENUM('ACTIVE','MATURED','FOLLOWUP','REINVESTED','CLOSED'),
              current_stage ENUM('F10','F5','F3','F1','MT','P30'),
              FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
            );
        """))

        # Create followup_log table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS followup_log (
              log_id CHAR(36) PRIMARY KEY,
              investment_id CHAR(36),
              stage ENUM('F10','F5','F3','F1','MT','P30'),
              sent_on DATETIME,
              FOREIGN KEY(investment_id) REFERENCES investment(investment_id)
            );
        """))
        print("Tables created successfully.")
    
    # Properly dispose of the engine to close connections and avoid "Event loop is closed" errors
    await engine.dispose()

if __name__ == "__main__":
    if not all([db_user, db_password, db_host, db_port, db_name]):
        print("Error: Cannot connect to database. Please set DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, and DB_NAME in .env")
    else:
        asyncio.run(create_tables())
