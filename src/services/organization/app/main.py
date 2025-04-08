from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import route as organization_route

app = FastAPI(
    title="Organization Service API",
    version="1.0.0",
    openapi_url='/organization-openapi.json'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(organization_route.router, prefix="/api/v1/organizations", tags=["organizations"])