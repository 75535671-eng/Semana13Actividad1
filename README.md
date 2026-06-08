# Proyecto Angular + FastAPI + Firebase

Aplicación full-stack con:
- **Frontend**: Angular 19
- **Backend**: FastAPI (Python)
- **Base de datos**: Firebase (Firestore + Realtime Database)

## Estructura del proyecto

```
semana 13/
├── frontend/          # Aplicación Angular
├── backend/           # API REST con FastAPI
├── firebase-rules.example.json
└── README.md
```

## Requisitos previos

- Node.js 18+ y npm
- Python 3.10+
- Cuenta en [Firebase Console](https://console.firebase.google.com/)

## Configuración de Firebase

### 1. Crear proyecto en Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com/) y crea un proyecto.
2. Habilita **Firestore Database** (modo prueba para desarrollo).
3. Habilita **Realtime Database** (modo prueba para desarrollo).

### 2. Credenciales del Admin SDK (backend)

1. Firebase Console → Configuración del proyecto → **Cuentas de servicio**.
2. Genera una nueva clave privada (JSON).
3. Guarda el archivo como `backend/firebase-service-account.json`.

### 3. Configuración del frontend

1. Firebase Console → Configuración del proyecto → **Tus apps** → Agregar app web.
2. Copia la configuración en `frontend/src/environments/environment.ts`.

### 4. Variables de entorno del backend

```bash
cd backend
copy .env.example .env
```

Edita `.env`:

```env
FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json
FIREBASE_DATABASE_URL=https://TU-PROYECTO-default-rtdb.firebaseio.com
CORS_ORIGINS=http://localhost:4200
```

## Instalación y ejecución

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API disponible en: http://localhost:8000  
Documentación Swagger: http://localhost:8000/docs

### Frontend (Angular)

```bash
cd frontend
npm install
npm start
```

App disponible en: http://localhost:4200

## Endpoints de la API

### Firestore — Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/firestore/tasks` | Listar tareas |
| GET | `/api/firestore/tasks/{id}` | Obtener tarea |
| POST | `/api/firestore/tasks` | Crear tarea |
| PUT | `/api/firestore/tasks/{id}` | Actualizar tarea |
| DELETE | `/api/firestore/tasks/{id}` | Eliminar tarea |

### Realtime Database — Mensajes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/realtime/messages` | Listar mensajes |
| POST | `/api/realtime/messages` | Crear mensaje |
| DELETE | `/api/realtime/messages/{id}` | Eliminar mensaje |

## Funcionalidades del frontend

- **Firestore (Tareas)**: CRUD de tareas vía API FastAPI.
- **Realtime DB (Chat)**: Envío y lectura de mensajes con actualización automática cada 3 segundos.

El servicio `FirebaseService` también incluye métodos para conectar directamente desde Angular a Firebase (cliente SDK), útil para escenarios en tiempo real sin pasar por la API.

## Reglas de seguridad (desarrollo)

Para desarrollo local, puedes usar reglas permisivas (ver `firebase-rules.example.json`).  
**En producción**, restringe el acceso con autenticación.

## Tecnologías

| Capa | Tecnología |
|------|------------|
| Frontend | Angular 19, Angular Fire, RxJS |
| Backend | FastAPI, Uvicorn, Pydantic |
| Base de datos | Firebase Firestore, Firebase Realtime Database |
| SDK | firebase-admin (backend), @angular/fire (frontend) |
