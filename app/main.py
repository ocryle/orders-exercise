import asyncio
import logging
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from app import config
from app.api import router
from app.consumer import consume
from app.db import engine

logging.basicConfig(level=config.LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(consume())
    logger.info("Orders API and consumer started")
    try:
        yield
    finally:
        if task.done() and not task.cancelled():
            task.exception()
        else:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        await engine.dispose()


app = FastAPI(title="Orders service", lifespan=lifespan)
app.include_router(router)
