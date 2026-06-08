import time

from app.firebase import get_realtime_ref
from app.models import MessageCreate, MessageResponse

MESSAGES_PATH = "messages"


def list_messages() -> list[MessageResponse]:
    ref = get_realtime_ref(MESSAGES_PATH)
    data = ref.get() or {}
    messages = []
    for msg_id, msg_data in data.items():
        if isinstance(msg_data, dict):
            messages.append(
                MessageResponse(
                    id=msg_id,
                    user=msg_data.get("user", ""),
                    text=msg_data.get("text", ""),
                    timestamp=msg_data.get("timestamp"),
                )
            )
    messages.sort(key=lambda m: m.timestamp or 0, reverse=True)
    return messages


def create_message(message: MessageCreate) -> MessageResponse:
    ref = get_realtime_ref(MESSAGES_PATH)
    new_ref = ref.push(
        {
            "user": message.user,
            "text": message.text,
            "timestamp": time.time(),
        }
    )
    data = new_ref.get()
    return MessageResponse(
        id=new_ref.key,
        user=data.get("user", ""),
        text=data.get("text", ""),
        timestamp=data.get("timestamp"),
    )


def delete_message(message_id: str) -> bool:
    ref = get_realtime_ref(f"{MESSAGES_PATH}/{message_id}")
    if ref.get() is None:
        return False
    ref.delete()
    return True
