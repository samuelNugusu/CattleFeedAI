from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

# Define the base directory (CattlefeedAI/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Mount the frontend directory to serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend"), name="static")

# Serve the index.html file at the root URL
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(BASE_DIR / "frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())

# Add a health check endpoint to verify the server is running
@app.get("/health")
async def health_check():
    return {"status": "Server is running"}