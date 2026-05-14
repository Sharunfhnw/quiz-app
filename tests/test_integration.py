import pytest
import hashlib

from sqlmodel import SQLModel, create_engine, Session, select


@pytest.fixture(name='session')
def session_fixture():
    from domain.models import (
        User, Quiz, Question,
        AnswerOption, QuizAttempt, StudentAnswer
    )
    engine = create_engine('sqlite:///:memory:')
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


# TC_010 - Quiz veröffentlichen
def test_quiz_veroeffentlichen(session):
    from domain.models import User, Quiz

    lehrer = User(
        username='l', email='l@t.ch',
        password_hash=hashlib.sha256(b'p').hexdigest(),
        role='teacher'
    )
    session.add(lehrer)
    session.commit()
    quiz = Quiz(
        title='Test', description='Test',
        is_published=False, teacher_id=lehrer.id
    )
    session.add(quiz)
    session.commit()
    quiz.is_published = True
    session.add(quiz)
    session.commit()
    result = session.get(Quiz, quiz.id)
    assert result.is_published == True
