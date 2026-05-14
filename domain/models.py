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



    class AnswerOption(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    is_correct: bool
    question_id: int = Field(foreign_key='question.id')
class QuizAttempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key='user.id')
    quiz_id: int = Field(foreign_key='quiz.id')
    score: int
    max_score: int
    completed_at: datetime = Field(default_factory=datetime.now)
class StudentAnswer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: int = Field(foreign_key='quizattempt.id')
    question_id: int = Field(foreign_key='question.id')
    selected_answer_option_id: int = Field(foreign_key='answeroption.id')
    is_correct: bool



   
    









from sqlmodel import Session, select
from domain.models import User, Quiz, Question
from domain.models import AnswerOption, QuizAttempt, StudentAnswer
class UserDAO:
    def __init__(self, session: Session):
        self.session = session
    def get_by_username(self, username: str):
        return self.session.exec(
            select(User).where(User.username == username)
        ).first()
    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user
class QuizDAO:
    def __init__(self, session: Session):
        self.session = session
    def get_published(self):
        return self.session.exec(
            select(Quiz).where(Quiz.is_published == True)
        ).all()
    def get_by_teacher(self, teacher_id: int):
        return self.session.exec(
            select(Quiz).where(Quiz.teacher_id == teacher_id)
        ).all()
    def save(self, quiz: Quiz) -> Quiz:
        self.session.add(quiz)
        self.session.commit()
        return quiz