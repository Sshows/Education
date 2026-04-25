from fastapi import FastAPI

from app.api.routes import router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="ent-grant-api")
app.include_router(router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}
