from pydantic import BaseModel

from models import Case
from schemas.Case import CaseType


class CreateCommand(BaseModel):
    Name: str
    case_id: int


class CommandType(BaseModel):
    id: int
    Name: str
    status: str
    case: CaseType

