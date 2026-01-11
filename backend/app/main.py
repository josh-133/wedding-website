import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import rsvp, registry, admin
from . import config

# Configure logging
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and check security on startup."""
    init_db()
    config.check_security_config()
    yield


app = FastAPI(
    title="Wedding RSVP API",
    description="API for Isabella and Joshua's wedding RSVP system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
# Get allowed origins from environment or use defaults for development
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rsvp.router)
app.include_router(registry.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Wedding RSVP API", "docs": "/docs"}
