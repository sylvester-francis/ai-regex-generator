"""
AI Regex Generator - FastAPI Application
Main entry point for the application
"""
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes import router as api_router
from app.routes.views import router as views_router
from app.database import create_db_and_tables

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Regex Generator",
    description="Generate regular expressions using AI",
    version="1.0.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(api_router, prefix="/api")
app.include_router(views_router)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()

# Root redirect
@app.get("/")
async def redirect_to_home():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/home")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)