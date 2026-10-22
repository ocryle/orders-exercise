import json
import logging

from aiokafka import AIOKafkaConsumer, TopicPartition
from sqlalchemy.ext.asyncio import AsyncSession

from app import config
from app.db import Session

logger = logging.getLogger(__name__)


async def handle_order_event(message: dict, session: AsyncSession) -> None:
    """Handle a full order snapshot from Kafka.

    Possible statuses: placed, shipped, delivered, cancelled

    New order:

    {
      "order_id": 1001,
      "customer_id": "acme",
      "status": "placed",
      "total_cents": 12500,
      "currency": "EUR",
      "items": [
        {"sku": "PAPER-A4", "quantity": 10},
        {"sku": "PEN-BLUE", "quantity": 20}
      ]
    }

    Updated snapshot:

    {
      "order_id": 1001,
      "customer_id": "acme",
      "status": "shipped",
      "total_cents": 12500,
      "currency": "EUR",
      "items": [
        {"sku": "PAPER-A4", "quantity": 10},
        {"sku": "PEN-BLUE", "quantity": 20}
      ]
    }

    """
    raise NotImplementedError("Validate and persist the order snapshot")


async def consume() -> None:
    consumer = AIOKafkaConsumer(
        config.KAFKA_TOPIC,
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=json.loads,
    )
    try:
        await consumer.start()
        logger.info("Listening on %s", config.KAFKA_TOPIC)
        async for record in consumer:
            async with Session.begin() as session:
                await handle_order_event(record.value, session)
            partition = TopicPartition(record.topic, record.partition)
            await consumer.commit({partition: record.offset + 1})
            logger.info("Processed partition=%s offset=%s", record.partition, record.offset)
    except Exception:
        logger.exception("Order consumer stopped")
        raise
    finally:
        await consumer.stop()
