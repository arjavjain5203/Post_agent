
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from backend.app.core.config import settings
import ssl

# Construct connect_args for SSL if enabled
connect_args = {}
if settings.DB_SSL:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connect_args['ssl'] = ctx

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_recycle=1800,
    pool_pre_ping=True,
    connect_args=connect_args
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as session:
        yield session
