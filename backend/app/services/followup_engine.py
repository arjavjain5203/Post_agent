from datetime import date, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.app.core.database import SessionLocal
from backend.app.models.base import Investment, Customer, FollowupLog, Agent
from backend.app.services import whatsapp_service
from backend.app.schemas.investment import StageEnum, InvestmentStatus
from backend.app.core.security import decrypt_field

async def check_daily_followups():
    """
    Cron job function.
    Scans investments and triggers notifications for due stages.
    """
    print(f"--- Running Daily Follow-up Scan: {date.today()} ---")
    
    async with SessionLocal() as db:
        today = date.today()
        
        # Get active investments
        # We need to join Customer to get Agent ID? Or just use customer->agent link later.
        # We need Customer mobile/name for the template, but we notify the AGENT.
        # So: Investment -> Customer -> Agent
        
        # Optimization: Fetch only ACTIVE investments
        # Note: In real production, batch this.
        stmt = select(Investment).where(
            Investment.status.in_([InvestmentStatus.ACTIVE, InvestmentStatus.FOLLOWUP])
        ).options(joinedload(Investment.customer_id)) 
        # joinedload might not work easily if relationship not defined in ORM models.
        # Let's define relationships in models/base.py first? 
        # Or just lazy load / query manually if relationships are missing.
        # Given we didn't add relationships in models yet, let's query manually or use foreign keys/joins.
        
        # Let's assume we didn't define `relationship` in models/base.py (we didn't).
        # We'll do a join in the select.
        stmt = select(Investment, Customer, Agent).join(
            Customer, Investment.customer_id == Customer.customer_id
        ).join(
            Agent, Customer.agent_id == Agent.agent_id
        ).where(
            Investment.status.in_([InvestmentStatus.ACTIVE, InvestmentStatus.FOLLOWUP])
        )
        
        result = await db.execute(stmt)
        rows = result.all()
        
        for investment, customer, agent in rows:
            maturity = investment.maturity_date
            days_diff = (maturity - today).days
            
            # Determine Trigger
            trigger_stage = None
            
            if days_diff == 10:
                trigger_stage = StageEnum.F10
            elif days_diff == 5:
                trigger_stage = StageEnum.F5
            elif days_diff == 3:
                trigger_stage = StageEnum.F3
            elif days_diff == 1:
                trigger_stage = StageEnum.F1
            elif days_diff == 0:
                trigger_stage = StageEnum.MT
            elif days_diff == -30:
                trigger_stage = StageEnum.P30
            
            if trigger_stage:
                # Check if already logged (to avoid duplicate runs if job runs logic twice or restarts)
                # Ideally, check FollowupLog for this investment + stage
                existing_log = await db.execute(
                    select(FollowupLog).where(
                        FollowupLog.investment_id == investment.investment_id,
                        FollowupLog.stage == trigger_stage
                    )
                )
                if existing_log.scalars().first():
                    continue

                # Process Trigger
                print(f"Triggering {trigger_stage} for Inv {investment.investment_id}")
                
                # Decrypt customer name for the message
                cust_name = "Customer"
                try:
                    full_name_val = customer.full_name
                    if isinstance(full_name_val, bytes):
                        full_name_val = full_name_val.decode('utf-8')
                    
                    if full_name_val:
                         cust_name = decrypt_field(full_name_val)
                except Exception as e:
                    print(f"Error decrypting name: {e}")
                
                # Notify Agent
                # Template params: [AgentName, CustomerName, Scheme, Amount, DaysRemaining]
                params = [
                    agent.name,
                    cust_name,
                    investment.scheme_type,
                    str(investment.principal),
                    str(days_diff) if days_diff >= 0 else "Overdue"
                ]
                
                await whatsapp_service.send_whatsapp_template(
                    to_mobile=agent.mobile,
                    template_name="investment_maturity_alert", # Hypothetical template
                    params=params
                )
                
                # Log it
                log = FollowupLog(
                    investment_id=investment.investment_id,
                    stage=trigger_stage,
                    sent_on=date.today()
                )
                db.add(log)
                
                # Update Investment Status/Stage
                investment.current_stage = trigger_stage
                if trigger_stage == StageEnum.MT:
                    investment.status = InvestmentStatus.MATURED
                else:
                    investment.status = InvestmentStatus.FOLLOWUP
                
                # db.add(investment) # Already tracked
        
        await db.commit()
