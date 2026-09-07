markdown
# ARCANA Installation Guide

ARCANA is designed to make installation simple and worry-free.

## Requirements
- Python 3.10+
- FastAPI
- Uvicorn
- Render (optional for deployment)

## Steps

### 1. Clone the repository
git clone <your-repo-url>
cd arcana-suite

Code

### 2. Install dependencies
pip install -r requirements.txt

Code

### 3. Start the backend
uvicorn backend.app:app --host 0.0.0.0 --port 10000

Code

### 4. Open the frontend
Serve the `frontend/` folder using any static host or Render static site.

## Safe Defaults
ARCANA installs with:
- offline mode
- user-level permissions
- safe install path `/usr/local/arcana`

Unsafe configurations are automatically rejected.
