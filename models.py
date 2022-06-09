from enum import Enum
from typing import Optional, List, Union
from uuid import UUID, uuid4
from pydantic import BaseModel, BaseSettings

class Gender(str, Enum):
    male: str = "male"
    female: str = "female"

class Role(str, Enum):
    admin: str = "admin"
    user: str = "user"

class Player(BaseModel):
    id: UUID
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    middle_name: Union[str, None] = None
    gender: Union[Gender, None] = None
    roles: Union[List[Role], None] = None

class PlayerUpdateRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    gender: Optional[Gender]
    roles: Optional[List[Role]]

class Games(BaseModel):
    id: UUID
    set_of_q: int
    round: int
    state_of_game: int

class GamesIN(BaseModel):
    set_of_q: int
    round: int
    state_of_game: int

class GameResult(BaseModel):
    id_player: UUID
    id_game: UUID
    result: int

class Questions(BaseModel):
    id: UUID
    question: Union[str, None] = None
    answers: Union[List[str], None] = None
    set: Union[List[int], None] = None

class QuestionsIN(BaseModel):
    question: str
    answers: List[str]
    set: List[int]

class Settings(BaseSettings):
    etag:UUID = uuid4()