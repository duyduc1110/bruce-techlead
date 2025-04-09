import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app import routes, db as database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Feedback Service API",
    version="1.0.0",
    docs_url='/docs',
    openapi_url='/feedback-openapi.json',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.member_router, prefix="/api/v1/organizations", tags=["Members"])