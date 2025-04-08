from pydantic import BaseModel

class OrganizationBase(BaseModel):
    name: str

class OrganizationResponse(OrganizationBase):
    id: int

    class Config:
        orm_mode = True