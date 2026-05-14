import pytest
from sqlmodel import SQLModel, create_engine, Session, select
@pytest.fixture(name='session')
def session_fixture():
    from domain.models import (
        User, Quiz, Question,
        AnswerOption, QuizAttempt, StudentAnswer
    )
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
# TC_007 — User wird korrekt gespeichert
def test_user_speichern(session):
    import hashlib
    from domain.models import User
    user = User(
        username='testlehrer',
        email='t@t.ch',
        password_hash=hashlib.sha256(b'pass').hexdigest(),
        role='teacher'
    )
    session.add(user)
    session.commit()
    result = session.exec(select(User)).first()
    assert result is not None
    assert result.role == 'teacher'



    # TC_008 — Quiz wird korrekt gespeichert
def test_quiz_speichern(session):
    import hashlib
    from domain.models import User, Quiz
    user = User(
        username='lehrer1',
        email='l@t.ch',
        password_hash=hashlib.sha256(b'p').hexdigest(),
        role='teacher'
    )
    session.add(user)
    session.commit()
    quiz = Quiz(
        title='Mathe',
        description='Test',
        is_published=False,
        teacher_id=user.id
    )
    session.add(quiz)
    session.commit()
    result = session.exec(select(Quiz)).first()
    assert result is not None
    assert result.is_published == False
# TC_009 — Leere Datenbank gibt keine Quizze zurueck
def test_leere_db(session):
    from domain.models import Quiz
    result = session.exec(select(Quiz)).all()
    assert len(result) == 0