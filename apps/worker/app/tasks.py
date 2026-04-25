from datetime import datetime

from app.ingestion import fetch_and_store_source


def fetch_source_task(source_id: int):
    return fetch_and_store_source(source_id=source_id, started_at=datetime.utcnow())
