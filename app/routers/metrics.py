from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_session
from ..models import DailyChecklist, OptionPositionSnapshot
from ..schemas import MetricsPreview

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/preview", response_model=MetricsPreview)
async def metrics_preview(session: AsyncSession = Depends(get_session)):
    # Example: last snapshot counts; adjust to your logic
    open_csp_count = await session.scalar(
        select(func.coalesce(func.count(), 0)).select_from(OptionPositionSnapshot)
    ) or 0

    # TODO: set from real calc; placeholder uses latest checklist
    latest = await session.scalar(
        select(DailyChecklist).order_by(DailyChecklist.created_at.desc())
    )

    return MetricsPreview(
        open_csp_count=open_csp_count,
        any_over_50pct_returned=False,   # compute once you ingest marks/credits
        cash_deployed_pct=float(latest.cash_deployed_pct) if latest and latest.cash_deployed_pct else 0.0,
    )
