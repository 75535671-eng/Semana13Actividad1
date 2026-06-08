# Configuración — Sem13-Actividad-IngWeb

Proyecto Firebase: **sem13-actividad-ingweb**

## Ya configurado automáticamente

- `frontend/src/environments/environment.ts` — credenciales del proyecto
- `frontend/google-services.json` — archivo Android copiado desde Descargas
- `backend/.env` — URLs del proyecto

## Paso 1: Reglas de Firestore (IMPORTANTE)

En Firebase Console → Firestore → pestaña **Reglas**, pega esto:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /tasks/{taskId} {
      allow read, write: if true;
    }
  }
}
```

Haz clic en **Publicar**.

## Paso 2: Activar Realtime Database (para el Chat)

1. Firebase Console → **Realtime Database** → **Crear base de datos**
2. Elige modo **prueba** (para desarrollo)
3. Copia la URL y verifica que coincida con:
   `https://sem13-actividad-ingweb-default-rtdb.firebaseio.com`
4. En **Reglas**, pega el contenido de `database.rules.json`

## Paso 3: Cuenta de servicio (solo para el backend FastAPI)

1. Firebase Console → ⚙️ **Configuración** → **Cuentas de servicio**
2. Clic en **Generar nueva clave privada**
3. Guarda el archivo JSON como:
   ```
   backend/firebase-service-account.json
   ```

Sin este archivo el **frontend funciona igual** (conexión directa a Firebase).
El backend necesita este archivo para operar.

## Paso 4: Ejecutar la aplicación

### Frontend (Angular)
```bash
cd frontend
npm install
npm start
```
Abre: http://localhost:4200

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8001
```
API: http://localhost:8001/docs

## Probar Firestore

1. Abre http://localhost:4200
2. Ve a **Firestore (Tareas)**
3. Agrega una tarea
4. Verifica en Firebase Console → Firestore → colección `tasks`
