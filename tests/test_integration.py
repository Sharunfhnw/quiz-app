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


# TC_011 - Schüler löst Quiz, Attempt gespeichert
def test_quiz_loesen(session):
    from domain.models import User, Quiz, QuizAttempt

    lehrer = User(username='l2', email='l2@t.ch',
        password_hash=hashlib.sha256(b'p').hexdigest(), role='teacher')
    schueler = User(username='s1', email='s1@t.ch',
        password_hash=hashlib.sha256(b'p').hexdigest(), role='student')
    session.add(lehrer)
    session.add(schueler)
    session.commit()
    quiz = Quiz(title='Mathe', description='Test',
        is_published=True, teacher_id=lehrer.id)
    session.add(quiz)
    session.commit()
    attempt = QuizAttempt(
        student_id=schueler.id, quiz_id=quiz.id,
        score=1, max_score=1
    )
    session.add(attempt)
    session.commit()
    result = session.get(QuizAttempt, attempt.id)
    assert result.score == 1


# TC_012 - Schüler löst Quiz zweimal
def test_quiz_zweimal_loesen(session):
    from domain.models import User, Quiz, QuizAttempt

    lehrer = User(username='l3', email='l3@t.ch',
        password_hash=hashlib.sha256(b'p').hexdigest(), role='teacher')
    schueler = User(username='s2', email='s2@t.ch',
        password_hash=hashlib.sha256(b'p').hexdigest(), role='student')
    session.add(lehrer)
    session.add(schueler)
    session.commit()
    quiz = Quiz(title='Englisch', description='Test',
        is_published=True, teacher_id=lehrer.id)
    session.add(quiz)
    session.commit()
    session.add(QuizAttempt(student_id=schueler.id,
        quiz_id=quiz.id, score=2, max_score=5))
    session.add(QuizAttempt(student_id=schueler.id,
        quiz_id=quiz.id, score=4, max_score=5))
    session.commit()
    attempts = session.exec(select(QuizAttempt).where(
        QuizAttempt.student_id == schueler.id)).all()
    assert len(attempts) == 2
