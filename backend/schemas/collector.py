from pydantic import BaseModel

class CollectorCreate(BaseModel):
    content: str
    label: str

class CollectorResponse(BaseModel):
    id: int
    content: str
    label: str

    class Config:
        from_attributes = True