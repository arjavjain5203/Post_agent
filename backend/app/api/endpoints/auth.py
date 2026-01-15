from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta, datetime

from backend.app.core.database import get_db
from backend.app.core.security import verify_password, get_password_hash, create_access_token
from backend.app.core.config import settings
from backend.app.models.base import Agent
from backend.app.services.sms import sms_service
from backend.app.schemas.auth import Token, AgentCreate, AgentLogin, AgentResponse, VerifyOTP, ResendOTP
from backend.app.api.deps import get_current_agent
import random

router = APIRouter()

@router.post("/signup", response_model=None)
async def signup(agent_in: AgentCreate, db: AsyncSession = Depends(get_db)):
    # Check if agent exists
    result = await db.execute(select(Agent).where(Agent.mobile == agent_in.mobile))
    agent = result.scalars().first()
    if agent:
        raise HTTPException(
            status_code=400,
            detail="Agent with this mobile number already registered",
        )
    
    # Generate OTP
    otp = str(random.randint(100000, 999999))
    import datetime as dt # avoid local var conflict
    expires_at = datetime.now() + timedelta(minutes=10)

    # Create new agent
    new_agent = Agent(
        name=agent_in.name,
        mobile=agent_in.mobile,
        password_hash=get_password_hash(agent_in.password),
        is_verified=False,
        verification_code=otp,
        verification_code_expires_at=expires_at
    )
    db.add(new_agent)
    await db.commit()
    await db.refresh(new_agent)
    
    # Send SMS
    sms_service.send_verification_code(new_agent.mobile, otp)
    
    return {"message": "Signup successful. Please verify OTP sent to your mobile."}

@router.post("/verify", response_model=None)
async def verify_otp(verify_data: VerifyOTP, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agent).where(Agent.mobile == verify_data.mobile))
    agent = result.scalars().first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    if agent.is_verified:
         raise HTTPException(status_code=400, detail="Agent already verified")

    if not agent.verification_code or agent.verification_code != verify_data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
        
    if agent.verification_code_expires_at and datetime.now() > agent.verification_code_expires_at:
        raise HTTPException(status_code=400, detail="OTP Expired")
        
    # Success
    agent.is_verified = True
    agent.verification_code = None
    agent.verification_code_expires_at = None
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    
    # Generate Token (Auto-login)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=agent.agent_id, expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False,
    )
    
    return {"message": "Verification successful."}

@router.post("/resend-otp", response_model=None)
async def resend_otp(resend_data: ResendOTP, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agent).where(Agent.mobile == resend_data.mobile))
    agent = result.scalars().first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    if agent.is_verified:
        raise HTTPException(status_code=400, detail="Agent already verified")

    # Generate new OTP
    otp = str(random.randint(100000, 999999))
    expires_at = datetime.now() + timedelta(minutes=10)
    
    agent.verification_code = otp
    agent.verification_code = otp
    agent.verification_code_expires_at = expires_at
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    
    # Send SMS
    if sms_service.send_verification_code(agent.mobile, otp):
        return {"message": "OTP resent successfully."}
    else:
        # In mock mode (no creds), this will still return success printed to console
        return {"message": "OTP resent (Simulated). check console if no creds."}

@router.post("/login", response_model=None)
async def login(login_data: AgentLogin, response: Response, db: AsyncSession = Depends(get_db)):
    # Find agent
    result = await db.execute(select(Agent).where(Agent.mobile == login_data.mobile))
    agent = result.scalars().first()
    
    if not agent:
        # To prevent user enumeration, we should theoretically simulate work here, 
        # but for now just return 401.
        raise HTTPException(status_code=401, detail="Incorrect mobile or password")
    
    # Check Lockout
    if agent.locked_until and agent.locked_until > datetime.now():
        raise HTTPException(
            status_code=401, 
            detail=f"Account locked. Try again after {agent.locked_until}"
        )

    if not agent.is_verified:
        raise HTTPException(status_code=403, detail="Account not verified. Please verify OTP.")

    # Verify Password
    if not verify_password(login_data.password, agent.password_hash):
        # Increment failure count
        agent.failed_login_attempts = (agent.failed_login_attempts or 0) + 1
        
        if agent.failed_login_attempts >= 5:
            agent.locked_until = datetime.now() + timedelta(minutes=15)
        
        await db.commit() # Save failure count
        
        raise HTTPException(status_code=401, detail="Incorrect mobile or password")
    
    # Reset failures on success
    if agent.failed_login_attempts > 0 or agent.locked_until:
        agent.failed_login_attempts = 0
        agent.locked_until = None
        db.add(agent)
        await db.commit()
        await db.refresh(agent)

    # Generate Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=agent.agent_id, expires_delta=access_token_expires
    )
    
    # Set HttpOnly Cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False, # Set True in Prod with HTTPS
    )
    
    return {"message": "Login successful"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}

@router.get("/me", response_model=AgentResponse)
async def read_users_me(current_agent: Agent = Depends(get_current_agent)):
    return current_agent
