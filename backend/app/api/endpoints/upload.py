from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from io import BytesIO

from backend.app.api import deps
from backend.app.core.database import get_db
from backend.app.models.base import Agent
from backend.app.schemas.customer import CustomerCreate
from backend.app.schemas.investment import InvestmentCreate, SchemeType, InvestmentStatus
from backend.app.services import customer_service, investment_service
from datetime import datetime

router = APIRouter()

@router.post("/bulk", status_code=201)
async def bulk_upload(
    file: UploadFile = File(...),
    current_agent: Agent = Depends(deps.get_current_agent),
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Invalid file format. Use Excel or CSV.")
    
    contents = await file.read()
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(contents))
        else:
            df = pd.read_excel(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse file: {str(e)}")

    # Expected columns: Name, Mobile, Scheme, Principal, StartDate, MaturityDate
    required_cols = ['Name', 'Mobile', 'Scheme', 'Principal', 'StartDate', 'MaturityDate']
    if not all(col in df.columns for col in required_cols):
        raise HTTPException(status_code=400, detail=f"Missing columns. Required: {required_cols}")

    # Get existing customers to deduplicate (by mobile)
    # Note: Optimization needed for large scale, but fine for MVP
    # We decrypt all agent's customers to check mobile numbers
    existing_customers = await customer_service.list_agent_customers(db, current_agent.agent_id)
    mobile_map = {c.mobile: c.customer_id for c in existing_customers} # mobile is already decrypted in list_agent_customers

    count_new_cust = 0
    count_inv = 0

    for _, row in df.iterrows():
        try:
            mobile = str(row['Mobile'])
            name = str(row['Name'])
            
            # 1. Get or Create Customer
            if mobile in mobile_map:
                customer_id = mobile_map[mobile]
            else:
                cust_in = CustomerCreate(full_name=name, mobile=mobile, consent_flag=False)
                new_cust = await customer_service.create_new_customer(db, cust_in, current_agent.agent_id)
                customer_id = new_cust.customer_id
                mobile_map[mobile] = customer_id # Cache it
                count_new_cust += 1

            # 2. Create Investment
            # Parse dates
            start_date = pd.to_datetime(row['StartDate']).date()
            mat_date = pd.to_datetime(row['MaturityDate']).date()
            
            scheme = row['Scheme'].upper()
            # Basic validation/mapping
            if scheme not in SchemeType.__members__:
                 # Fallback or skip? Let's skip invalid schemes for now
                 continue
                 
            inv_in = InvestmentCreate(
                customer_id=customer_id,
                scheme_type=SchemeType[scheme],
                principal=float(row['Principal']),
                start_date=start_date,
                maturity_date=mat_date,
                status=InvestmentStatus.ACTIVE
            )
            await investment_service.create_investment(db, inv_in)
            count_inv += 1
            
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

    return {"message": "Upload processed", "new_customers": count_new_cust, "investments_created": count_inv}
