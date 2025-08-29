"""
This is a simple entry point that imports the FastAPI app from the backend directory.
"""

from backend.main import app

# This allows the file to be run directly with: `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
