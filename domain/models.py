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


    from sqlmodel import create_engine, SQLModel, Session
class Database:
    def __init__(self, url: str = 'sqlite:///quiz.db'):
        self.engine = create_engine(url)
    def init_schema_and_seed(self):
        from data_access.seed import seed_data
        SQLModel.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            seed_data(session)
    def get_session(self):
        return Session(self.engine)
    

    import hashlib
from sqlmodel import Session, select
from domain.models import User, Quiz, Question, AnswerOption
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
def seed_data(session: Session) -> None:
    existing = session.exec(select(User)).first()
    if existing:
        return  # Bereits geseedet
    lehrer = User(
        username='lehrer',
        email='lehrer@quiz.ch',
        password_hash=hash_password('lehrer123'),
        role='teacher'
    )
    schueler = User(
        username='schueler',
        email='schueler@quiz.ch',
        password_hash=hash_password('schueler123'),
        role='student'
    )
    session.add(lehrer)
    session.add(schueler)
    session.commit()
    print('Demo-User erstellt!')


    


