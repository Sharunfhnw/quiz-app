
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