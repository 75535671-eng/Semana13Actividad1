# Desplegar en Render

Guía paso a paso para publicar el proyecto **Sem13-Actividad-IngWeb** en [Render](https://render.com).

## Requisitos

1. Cuenta en [Render](https://render.com) (gratis)
2. Repositorio en **GitHub** con este código
3. Clave de cuenta de servicio de Firebase (JSON)

---

## Paso 1: Subir el código a GitHub

```bash
cd "d:\Ingenieria Web\semana 13"
git init
git add .
git commit -m "Proyecto Angular + FastAPI + Firebase"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

---

## Paso 2: Crear el Blueprint en Render

1. Entra a [dashboard.render.com/blueprints](https://dashboard.render.com/blueprints)
2. Clic en **New Blueprint Instance**
3. Conecta tu repositorio de GitHub
4. Render detectará el archivo `render.yaml` y creará 2 servicios:
   - `sem13-backend` (FastAPI)
   - `sem13-frontend` (Angular estático)

---

## Paso 3: Configurar variables de entorno en Render

### Backend (`sem13-backend`)

Ve a **Environment** del servicio backend y agrega:

| Variable | Valor |
|----------|-------|
| `FIREBASE_CREDENTIALS_JSON` | Pega **todo** el contenido del archivo JSON de cuenta de servicio (en una sola línea) |
| `CORS_ORIGINS` | `https://sem13-frontend.onrender.com` (ajusta con tu URL real del frontend) |

> **Cómo obtener el JSON:** Firebase Console → ⚙️ Configuración → **Cuentas de servicio** → **Generar nueva clave privada**

### Frontend (`sem13-frontend`)

Si la URL de tu backend es diferente a `sem13-backend.onrender.com`, edita:

`frontend/src/environments/environment.prod.ts` → campo `apiUrl`

---

## Paso 4: Autorizar dominio en Firebase

1. Firebase Console → **Authentication** → **Settings** → **Authorized domains**
2. Agrega: `sem13-frontend.onrender.com` (tu dominio de Render)

También en **Firestore → Reglas**, asegúrate de tener permisos de lectura/escritura para desarrollo.

---

## Paso 5: Desplegar

1. En Render, clic en **Manual Deploy → Deploy latest commit** (o espera el deploy automático)
2. Espera a que ambos servicios estén en estado **Live** (verde)

### URLs resultantes

| Servicio | URL |
|----------|-----|
| Frontend | `https://sem13-frontend.onrender.com` |
| Backend API | `https://sem13-backend.onrender.com` |
| Swagger docs | `https://sem13-backend.onrender.com/docs` |

---

## Despliegue manual (sin Blueprint)

Si prefieres crear los servicios uno por uno:

### Backend
- **Tipo:** Web Service
- **Runtime:** Python 3
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend
- **Tipo:** Static Site
- **Root Directory:** `frontend`
- **Build Command:** `npm install && npm run build`
- **Publish Directory:** `dist/frontend/browser`
- **Rewrite:** `/*` → `/index.html`

---

## Notas importantes

- El plan **gratuito** de Render apaga el backend tras 15 min de inactividad (tarda ~30s en despertar).
- No subas `firebase-service-account.json` a GitHub; usa la variable `FIREBASE_CREDENTIALS_JSON`.
- El frontend se conecta **directo a Firebase**, así que funciona aunque el backend esté dormido.
