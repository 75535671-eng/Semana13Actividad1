from fastapi import APIRouter, HTTPException

from app.firebase import get_firebase_error, is_firebase_ready
from app.models import TaskCreate, TaskResponse, TaskUpdate
from app.services import firestore_service

router = APIRouter(prefix="/api/firestore", tags=["Firestore"])


def _ensure_firebase():
    if not is_firebase_ready():
        raise HTTPException(
            status_code=503,
            detail=get_firebase_error()
            or "Firebase no configurado. Coloca firebase-service-account.json en backend/",
        )


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    _ensure_firebase()
    return firestore_service.list_tasks()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    _ensure_firebase()
    task = firestore_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    _ensure_firebase()
    return firestore_service.create_task(task)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task: TaskUpdate):
    _ensure_firebase()
    updated = firestore_service.update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return updated


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    _ensure_firebase()
    if not firestore_service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
