from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.endpoints import auth, customers, investments, upload

from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from backend.app.services.followup_engine import check_daily_followups

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler = AsyncIOScheduler()
    # Run everyday at 9:00 AM
    scheduler.add_job(check_daily_followups, 'cron', hour=9, minute=0)
    # Also run once immediately on startup for Development/Verification
    scheduler.add_job(check_daily_followups, 'date')
    scheduler.start()
    
    print("-" * 40)
    print(f"ADMIN SECRET: {settings.ADMIN_SECRET}")
    print("-" * 40)
    
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS (Allow all for dev, restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"DEBUG HEADERS: {request.method} {request.url}")
    for name, value in request.headers.items():
        print(f"  {name}: {value}")
    response = await call_next(request)
    return response


# Include Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(customers.router, prefix=f"{settings.API_V1_STR}/customers", tags=["customers"])
app.include_router(investments.router, prefix=f"{settings.API_V1_STR}/investments", tags=["investments"])
app.include_router(upload.router, prefix=f"{settings.API_V1_STR}/upload", tags=["upload"])

from backend.app.api.endpoints import dashboard
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])

from backend.app.api.endpoints import admin
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])

@app.get("/")
def root():
    return {"message": "Welcome to Post Office Agent SaaS API"}
