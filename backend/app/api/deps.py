from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.models.base import Agent
from backend.app.schemas.auth import TokenData

async def get_current_agent(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Agent:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    token_str = request.cookies.get("access_token")
    if not token_str:
        # Check Authorization header as fallback (optional, useful for Swagger)
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token_str = auth_header
        else:
            raise credentials_exception
            
    # Strip "Bearer " if present
    if token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
    else:
        token = token_str

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        agent_id: str = payload.get("sub")
        if agent_id is None:
            raise credentials_exception
        token_data = TokenData(agent_id=agent_id)
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(Agent).where(Agent.agent_id == token_data.agent_id))
    agent = result.scalars().first()
    if agent is None:
        raise credentials_exception
    return agent

async def get_current_admin(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
    )
    
    token_str = request.cookies.get("access_token")
    # For Admin, we can also check header or just cookie
    if not token_str:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token_str = auth_header
        else:
             raise credentials_exception

    if token_str.startswith("Bearer "):
        token = token_str.split(" ")[1]
    else:
        token = token_str

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        role: str = payload.get("sub")
        if role != "admin":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return True
