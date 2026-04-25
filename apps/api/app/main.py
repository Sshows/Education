from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="ent-grant-api")
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
