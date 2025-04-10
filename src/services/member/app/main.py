import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app import routes, db as database
from app.seed_data import seed_members

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Member Service API",
    version="1.0.0",
    docs_url='/docs',
    openapi_url='/member-openapi.json', 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.member_router, prefix="/api/v1/organizations", tags=["Members"])

@app.on_event("startup")
async def seeding_members():
    db = next(database.get_db())
    print('Seeding data...')
    try:
        seed_members(db)
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()