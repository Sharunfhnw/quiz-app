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