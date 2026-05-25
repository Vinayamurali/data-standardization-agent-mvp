# Backend: Data Standardization Agent MVP

This FastAPI backend exposes APIs for a metadata-only data standardization agent.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Pandas
- OpenPyXL
- OpenAI SDK
- Pytest

## Run Backend

```powershell
cd C:\projects\data-standardization-agent-mvp\backend
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload