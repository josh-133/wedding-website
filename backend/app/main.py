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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
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
