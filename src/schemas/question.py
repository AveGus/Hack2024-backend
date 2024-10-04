from pydantic import BaseModel


class CreateQuestion(BaseModel):
    case_id: int
    text: str


class QuestionType(BaseModel):
    id: int
    case_id: int
    text: str
