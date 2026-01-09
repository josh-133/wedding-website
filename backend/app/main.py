from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import rsvp, registry, admin

app = FastAPI(
    title="Wedding RSVP API",
    description="API for Isabella and Joshua's wedding RSVP system",
    version="1.0.0"
)

# CORS configuration
import os

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


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {"message": "Wedding RSVP API", "docs": "/docs"}
