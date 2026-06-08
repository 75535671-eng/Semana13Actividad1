from app.firebase import get_firestore
from app.models import TaskCreate, TaskResponse, TaskUpdate

COLLECTION = "tasks"


def list_tasks() -> list[TaskResponse]:
    db = get_firestore()
    docs = db.collection(COLLECTION).stream()
    return [
        TaskResponse(
            id=doc.id,
            title=data.get("title", ""),
            description=data.get("description", ""),
            completed=data.get("completed", False),
        )
        for doc in docs
        if (data := doc.to_dict())
    ]


def get_task(task_id: str) -> TaskResponse | None:
    db = get_firestore()
    doc = db.collection(COLLECTION).document(task_id).get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    return TaskResponse(
        id=doc.id,
        title=data.get("title", ""),
        description=data.get("description", ""),
        completed=data.get("completed", False),
    )


def create_task(task: TaskCreate) -> TaskResponse:
    db = get_firestore()
    _, doc_ref = db.collection(COLLECTION).add(task.model_dump())
    return TaskResponse(id=doc_ref.id, **task.model_dump())


def update_task(task_id: str, task: TaskUpdate) -> TaskResponse | None:
    db = get_firestore()
    doc_ref = db.collection(COLLECTION).document(task_id)
    if not doc_ref.get().exists:
        return None
    updates = task.model_dump(exclude_unset=True)
    if updates:
        doc_ref.update(updates)
    return get_task(task_id)


def delete_task(task_id: str) -> bool:
    db = get_firestore()
    doc_ref = db.collection(COLLECTION).document(task_id)
    if not doc_ref.get().exists:
        return False
    doc_ref.delete()
    return True
