# run_local.ps1
# This script starts the backend API locally.
# Requirements: pip install uvicorn

uvicorn app:app --reload --port 8000
