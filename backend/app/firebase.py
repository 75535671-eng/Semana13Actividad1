import json
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, db, firestore

from app.config import settings

_firebase_app = None
_firestore_client = None
_firebase_error: str | None = None


def credentials_configured() -> bool:
    if settings.firebase_credentials_json.strip():
        return True
    return Path(settings.firebase_credentials_path).exists()


def _parse_credentials_json(raw: str) -> dict:
    raw = raw.strip()
    if not raw:
        raise ValueError("FIREBASE_CREDENTIALS_JSON está vacío.")

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Algunos paneles convierten \n literales en saltos de línea reales
        compact = " ".join(line.strip() for line in raw.splitlines())
        return json.loads(compact)


def _load_credentials():
    if settings.firebase_credentials_json.strip():
        return credentials.Certificate(_parse_credentials_json(settings.firebase_credentials_json))

    cred_path = Path(settings.firebase_credentials_path)
    if not cred_path.exists():
        raise FileNotFoundError(
            "Credenciales no configuradas. En Render agrega FIREBASE_CREDENTIALS_JSON "
            "o vincula el Environment Group firebase-sem13 al servicio sem13-backend."
        )
    return credentials.Certificate(str(cred_path))


def init_firebase() -> None:
    global _firebase_app, _firestore_client, _firebase_error

    if _firebase_app is not None:
        return

    if not settings.firebase_database_url:
        _firebase_error = "FIREBASE_DATABASE_URL no está configurada."
        raise ValueError(_firebase_error)

    if not credentials_configured():
        _firebase_error = (
            "FIREBASE_CREDENTIALS_JSON no está configurada en Render. "
            "Ve a sem13-backend → Environment → vincula firebase-sem13."
        )
        raise FileNotFoundError(_firebase_error)

    try:
        cred = _load_credentials()
        _firebase_app = firebase_admin.initialize_app(
            cred,
            {"databaseURL": settings.firebase_database_url},
        )
        _firestore_client = firestore.client()
        _firebase_error = None
    except Exception as exc:
        _firebase_error = str(exc)
        raise


def is_firebase_ready() -> bool:
    return _firebase_app is not None and _firestore_client is not None


def get_firebase_error() -> str | None:
    return _firebase_error


def get_firestore():
    if _firestore_client is None:
        init_firebase()
    return _firestore_client


def get_realtime_ref(path: str = "/"):
    if _firebase_app is None:
        init_firebase()
    return db.reference(path)
