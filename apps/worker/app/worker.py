"""RQ worker bootstrap for source ingestion and recalculation tasks."""

from redis import Redis
from rq import Worker, Queue


def main() -> None:
    redis = Redis(host="redis", port=6379, db=0)
    queue = Queue("ingestion", connection=redis)
    worker = Worker([queue], connection=redis)
    worker.work()


if __name__ == "__main__":
    main()
