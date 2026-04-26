from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.payments import admin_router as payments_admin_router
from app.api.payments import router as payments_router
from app.api.routes import router

app = FastAPI(title="ent-grant-api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
app.include_router(payments_router)
app.include_router(payments_admin_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "api"}
