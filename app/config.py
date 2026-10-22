import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://orders:orders@localhost:55433/orders")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:19092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "orders.snapshots")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "orders-projection")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
