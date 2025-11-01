from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import engine, Base
from .routers import health, checklist, metrics, positions

app = FastAPI(title="Option Checklist API")

# CORS
origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")] if settings.ALLOWED_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables at startup (simple MVP)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Routers
app.include_router(health.router)
app.include_router(checklist.router)
app.include_router(metrics.router)
app.include_router(positions.router)
