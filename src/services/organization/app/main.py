from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route import router as organization_route

app = FastAPI(
    title="Organization Service API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(organization_route.router, prefix="/api/v1/organizations", tags=["organizations"])

@app.get("/", tags=["health"])
def read_root():
    return {"status": "healthy", "service": "organization-service"}