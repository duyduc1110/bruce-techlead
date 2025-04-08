import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, routes

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Comment Service API",
    description="API for managing organization feedbacks",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.feedback_router, prefix="/api/v1/feedbacks", tags=["feedbacks"])

# Root endpoint for health checks
@app.get("/", tags=["health"])
def read_root():
    return {"status": "healthy", "service": "feedback-service"}