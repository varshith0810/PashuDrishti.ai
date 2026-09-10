
# Backend

## Core service
- `app.py`: FastAPI app, server-rendered UI routes, REST API endpoints, and session management.
- `db.py`: SQLite connection + initialization helpers.
- `schema.sql`: Canonical SQL schema for users and predictions.
- `app.db`: SQLite database file.
- `test_api.py`: Automated test suite testing all endpoints with diverse pictures.
- `create_test_images.py`: Generator for diverse cattle test pictures.

## Entrypoints

From repository root:
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

From inside `backend/` directory:
```powershell
./run_local.ps1
# or:
uvicorn app:app --reload --port 8000
```

## Running Automated Tests

Ensure the server is running on port 8000, then execute:
```bash
python backend/test_api.py
```

## API Endpoints

| Endpoint | Method | Format | Description |
| --- | --- | --- | --- |
| `/health` | GET | JSON | System health and model load status. |
| `/` | GET | HTML | Home page (redirects to `/signin` if unauthenticated). |
| `/signin` | GET, POST | HTML / JSON | Sign-in page and authentication handler. |
| `/create-account` | GET, POST | HTML / JSON | User registration page and handler. |
| `/logout` | GET | HTML / JSON | Clears user session. |
| `/predict` | POST | HTML / JSON | Image upload form handler & dual JSON API. |
| `/api/predict` | POST | JSON | Dedicated REST API for direct model inference. |
| `/api/predictions`| GET | JSON | Returns recent saved predictions for the logged-in user. |
| `/debug/bundle` | GET | JSON | Bundle diagnostic file listing (enabled via `DEBUG_BUNDLE=true`). |


