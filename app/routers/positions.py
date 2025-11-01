from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_session

router = APIRouter(prefix="/positions", tags=["positions"])

@router.post("/sync")
async def sync_positions(session: AsyncSession = Depends(get_session)):
    """
    TODO:
      - Use Schwab OAuth tokens (store later) or a market-data vendor
      - Pull open options, compute premium_returned_pct
      - Insert rows into OptionPositionSnapshot
    """
    # placeholder for now
    return {"synced": 0}
