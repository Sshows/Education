from datetime import datetime


def fetch_source_task(source_id: int):
    return {"source_id": source_id, "status": "queued", "timestamp": datetime.utcnow().isoformat()}
