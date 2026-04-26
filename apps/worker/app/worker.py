"""RQ worker bootstrap for source ingestion and recalculation tasks."""

import os

from redis import Redis
from rq import Worker, Queue


def main() -> None:
    redis = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    queue = Queue("ingestion", connection=redis)
    worker = Worker([queue], connection=redis)
    worker.work()


if __name__ == "__main__":
    main()
