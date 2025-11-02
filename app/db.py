import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from .config import settings

# Create SSL context explicitly (for DigitalOcean Postgres)
ssl_context = ssl.create_default_context(cafile=None)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

connect_args = {"ssl": ssl_context}

# Remove ?sslmode=require from the URL and pass the SSL context separately
engine = create_async_engine(
    settings.DATABASE_URL.replace("?sslmode=require", ""),
    echo=False,
    pool_pre_ping=True,
    connect_args=connect_args
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
