from fastapi import APIRouter, HTTPException

from app.firebase import get_firebase_error, is_firebase_ready
from app.models import MessageCreate, MessageResponse
from app.services import realtime_service

router = APIRouter(prefix="/api/realtime", tags=["Realtime Database"])


def _ensure_firebase():
    if not is_firebase_ready():
        raise HTTPException(
            status_code=503,
            detail=get_firebase_error()
            or "Firebase no configurado. Coloca firebase-service-account.json en backend/",
        )


@router.get("/messages", response_model=list[MessageResponse])
def get_messages():
    _ensure_firebase()
    return realtime_service.list_messages()


@router.post("/messages", response_model=MessageResponse, status_code=201)
def create_message(message: MessageCreate):
    _ensure_firebase()
    return realtime_service.create_message(message)


@router.delete("/messages/{message_id}", status_code=204)
def delete_message(message_id: str):
    _ensure_firebase()
    if not realtime_service.delete_message(message_id):
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
