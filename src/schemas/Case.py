from pydantic import BaseModel


class CaseCreateSchema(BaseModel):
    name: str
    description: str


class CaseType(BaseModel):
    id: int
    name: str
    description: str