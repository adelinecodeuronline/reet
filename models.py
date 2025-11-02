#User, mood, action

from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    points: int = 0
    tree_stage: int = 1 #étape mate virtuel (levels 1 à 5)
    karma: int = 50 #confiance
    mood: Optional[str] = None

class Action(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    mood: str
    type: str #social, self-care, contribution, créatif
    difficulty: int
    points: int
