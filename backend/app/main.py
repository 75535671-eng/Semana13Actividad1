from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.firebase import get_firebase_error, init_firebase, is_firebase_ready
from app.routers import firestore, realtime


@asynccontextmanager
async def lifespan(app: FastAPI):
    cred_path = Path(settings.firebase_credentials_path)
    has_credentials = bool(settings.firebase_credentials_json) or cred_path.exists()
    if has_credentials:
        try:
            init_firebase()
        except Exception:
            pass
    yield


app = FastAPI(
    title="Firebase API - Sem13-Actividad-IngWeb",
    description="API con FastAPI usando Firestore y Realtime Database de Firebase",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(firestore.router)
app.include_router(realtime.router)


@app.get("/")
def root():
    return {
        "message": "API Firebase - Sem13-Actividad-IngWeb",
        "project": "sem13-actividad-ingweb",
        "firebase_ready": is_firebase_ready(),
        "docs": "/docs",
        "endpoints": {
            "firestore": "/api/firestore/tasks",
            "realtime": "/api/realtime/messages",
        },
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "firebase_ready": is_firebase_ready(),
        "firebase_error": get_firebase_error(),
    }
