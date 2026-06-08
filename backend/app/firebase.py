import json
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, db, firestore

from app.config import settings

_firebase_app = None
_firestore_client = None
_firebase_error: str | None = None


def _load_credentials():
    if settings.firebase_credentials_json:
        return credentials.Certificate(json.loads(settings.firebase_credentials_json))

    cred_path = Path(settings.firebase_credentials_path)
    if not cred_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de credenciales: {cred_path}. "
            "En Render, configura la variable FIREBASE_CREDENTIALS_JSON. "
            "En local, descarga la clave desde Firebase Console > Cuentas de servicio."
        )
    return credentials.Certificate(str(cred_path))


def init_firebase() -> None:
    global _firebase_app, _firestore_client, _firebase_error

    if _firebase_app is not None:
        return

    if not settings.firebase_database_url:
        _firebase_error = "FIREBASE_DATABASE_URL no está configurada."
        raise ValueError(_firebase_error)

    try:
        cred = _load_credentials()
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        _firebase_error = str(exc)
        raise

    _firebase_app = firebase_admin.initialize_app(
        cred,
        {"databaseURL": settings.firebase_database_url},
    )
    _firestore_client = firestore.client()
    _firebase_error = None


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
