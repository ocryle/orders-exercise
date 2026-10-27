from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session

router = APIRouter()
DatabaseSession = Annotated[AsyncSession, Depends(get_session)]
CustomerId = Annotated[str | None, Query()]


@router.get("/orders", response_model=None)
async def list_orders(session: DatabaseSession, customer_id: CustomerId = None):
    raise NotImplementedError("Implement order listing")


@router.get("/orders/{order_id}", response_model=None)
async def get_order(order_id: int, session: DatabaseSession, customer_id: CustomerId = None):
    raise NotImplementedError("Implement order lookup")
