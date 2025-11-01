from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_session
from ..models import DailyChecklist
from ..schemas import DailyChecklistIn, DailyChecklistOut
from datetime import date

router = APIRouter(prefix="/checklist", tags=["checklist"])

@router.post("", response_model=DailyChecklistOut)
async def submit_checklist(payload: DailyChecklistIn, session: AsyncSession = Depends(get_session)):
    # Ensure one per day (unique user/day later—single user now)
    exists = await session.scalar(
        select(DailyChecklist).where(DailyChecklist.trade_date == payload.trade_date)
    )
    if exists:
        # Update existing
        for k, v in payload.model_dump().items():
            setattr(exists, k, v)
        await session.commit()
        await session.refresh(exists)
        return exists

    row = DailyChecklist(**payload.model_dump())
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row

@router.get("/today", response_model=DailyChecklistOut | None)
async def get_today(session: AsyncSession = Depends(get_session)):
    today = date.today()
    row = await session.scalar(select(DailyChecklist).where(DailyChecklist.trade_date == today))
    return row
