import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db import Base, get_session
from app.main import app


@pytest.fixture
async def sessions():
    from app import models  # noqa: F401

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    @event.listens_for(engine.sync_engine, "connect")
    def enable_foreign_keys(connection, _):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        await engine.dispose()


@pytest.fixture
async def client(sessions):
    async def test_session():
        async with sessions() as session:
            yield session

    app.dependency_overrides[get_session] = test_session
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
async def ingest(sessions):
    from app.consumer import handle_order_event

    async def ingest(message):
        async with sessions.begin() as session:
            await handle_order_event(message, session)

    return ingest


@pytest.fixture
def order_event():
    return {
        "order_id": 1001,
        "customer_id": "acme",
        "status": "placed",
        "total_cents": 12500,
        "currency": "EUR",
        "items": [{"sku": "PAPER-A4", "quantity": 10}, {"sku": "PEN-BLUE", "quantity": 20}],
    }
