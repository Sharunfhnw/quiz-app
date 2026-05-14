from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password_hash: str
    role: str  # 'teacher' oder 'student'


    class Quiz(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    is_published: bool = False
    teacher_id: int = Field(foreign_key='user.id')
class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    quiz_id: int = Field(foreign_key='quiz.id')