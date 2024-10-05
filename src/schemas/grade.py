import enum
from enum import Enum

from pydantic import BaseModel
from typing_extensions import Literal

class Grade (enum.IntEnum):
    bad = 1
    okay = 2
    good = 3
    very_good = 4
    perfect = 5


class GradeSchema(BaseModel):
    question_id: int
    command_id: int
    score: Literal[Grade.bad, Grade.okay, Grade.good, Grade.very_good, Grade.perfect]
