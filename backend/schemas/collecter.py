from pydantic import BaseModel

class CollecterCreate(BaseModel):
    content: str
    label: str

class CollecterResponse(BaseModel):
    id: int
    content: str
    label: str

    class Config:
        from_attributes = True