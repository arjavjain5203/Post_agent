from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from typing import List, Optional

from backend.app.models.base import Customer
from backend.app.schemas.customer import CustomerCreate
from backend.app.core.security import encrypt_field, decrypt_field

async def create_new_customer(db: AsyncSession, customer_in: CustomerCreate, agent_id: str) -> Customer:
    # Encrypt PII
    encrypted_name = encrypt_field(customer_in.full_name)
    encrypted_mobile = encrypt_field(customer_in.mobile)
    
    # Store binary/encrypted
    # Wait, encrypt_field returns base64 string "IV:TAG:CIPHER".
    # The DB column is LargeBinary(255).
    # We should probably store it as bytes or change column to Text if it's base64 encoded string.
    # The models/base.py defined it as LargeBinary(255). 
    # If the output of encrypt_field is a string (base64 encoded), we can encode it to bytes to store in LargeBinary, 
    # or just change model to String/Text.
    # Given the format "IV:TAG:CIPHER" can get long, 255 bytes might be tight if name is long.
    # 32 bytes (IV+TAG) + Ciphertext (Input length) + 2 colons. Base64 expands by 4/3.
    # Let's verify encrypt_field output. It returns string.
    # We will encode it to utf-8 bytes to store in LargeBinary.
    
    db_customer = Customer(
        agent_id=agent_id,
        full_name=encrypted_name.encode('utf-8'),
        mobile=encrypted_mobile.encode('utf-8'),
        consent_flag=customer_in.consent_flag,
        consent_time=datetime.now() if customer_in.consent_flag else None
    )
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

async def get_customer_by_id(db: AsyncSession, customer_id: str) -> Optional[Customer]:
    result = await db.execute(select(Customer).where(Customer.customer_id == customer_id))
    customer = result.scalars().first()
    if customer:
        db.expunge(customer) # Detach to avoid saving decrypted data back to DB
        decrypt_customer_in_place(customer)
    return customer

async def list_agent_customers(db: AsyncSession, agent_id: str) -> List[Customer]:
    result = await db.execute(select(Customer).where(Customer.agent_id == agent_id))
    customers = result.scalars().all()
    # Decrypt all for display
    # Note: iterating and decrypting might be slow for bulk, but necessary for encrypted DB.
    for cust in customers:
        db.expunge(cust) # Detach
        decrypt_customer_in_place(cust)
    return customers

def decrypt_customer_in_place(customer: Customer):
    """
    Helper to decrypt fields on a Customer model instance.
    We temporarily replace the binary content with the decrypted string for Pydantic response.
    """
    if customer.full_name:
        customer.full_name = decrypt_field(customer.full_name.decode('utf-8'))
    if customer.mobile:
        customer.mobile = decrypt_field(customer.mobile.decode('utf-8'))
