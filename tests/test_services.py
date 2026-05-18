"""Service layer tests for LearnLoop.
Tests TC_013 to TC_018 covering AuthService and QuizService.
All tests use an in-memory SQLite database so no file is created.
"""
import pytest
import hashlib
from sqlmodel import SQLModel, create_engine, Session
from services.auth_service import AuthService
from services.quiz_service import QuizService
@pytest.fixture(name='session')
def session_fixture():
    """Create a fresh in-memory database for each test."""
    from domain.models import (
        User, Quiz, Question, AnswerOption,
        QuizAttempt, StudentAnswer
    )
    # Use in-memory SQLite — no file created, resets after each test
    engine = create_engine('sqlite:///:memory:')
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


#  AuthService Tests 

# TC_013 — hash_password returns correct SHA256 hash
def test_hash_password_returns_sha256():
    """TC_013: hash_password() should return a valid SHA256 hash."""
    auth = AuthService()
    password = 'lehrer123'
    # Expected hash calculated manually
    expected = hashlib.sha256(password.encode()).hexdigest()
    result = auth.hash_password(password)
    assert result == expected
    # SHA256 hex digest is always 64 characters
    assert len(result) == 64
# TC_014 — check_password returns True for correct password
def test_check_password_correct():
    """TC_014: check_password() should return True for correct password."""
    auth = AuthService()
    password = 'meinPasswort123'
    stored_hash = auth.hash_password(password)
    # Same password should match the stored hash
    result = auth.check_password(password, stored_hash)
    assert result == True
# TC_015 — check_password returns False for wrong password
def test_check_password_wrong():
    """TC_015: check_password() should return False for wrong password."""
    auth = AuthService()
    stored_hash = auth.hash_password('richtigesPasswort')
    # Different password should NOT match
    result = auth.check_password('falschesPasswort', stored_hash)
    assert result == False
# TC_016 — login finds correct user
def test_login_finds_user(session):
    """TC_016: login() should return the correct User object."""
    from domain.models import User
    auth = AuthService()
    # Create a test user directly in the database
    user = User(
        username='testlehrer',
        email='test@learnloop.ch',
        password_hash=auth.hash_password('passwort123'),
        role='teacher'
    )
    session.add(user)
    session.commit()
    # Login with correct credentials should return the user
    result = auth.login(session, 'testlehrer', 'passwort123')
    assert result is not None
    assert result.username == 'testlehrer'
    assert result.role == 'teacher'


#  QuizService Tests

# TC_017 — get_published returns only published quizzes
def test_get_published_only_returns_published(session):
    """TC_017: get_published() should only return quizzes where
    is_published is True."""
    from domain.models import User, Quiz
    quiz_service = QuizService()
    # Create a teacher
    teacher = User(
        username='l', email='l@t.ch',
        password_hash='hash', role='teacher'
    )
    session.add(teacher)
    session.commit()
    # Create one published and one unpublished quiz
    q1 = Quiz(
        title='Veroeffentlicht', description='Test',
        is_published=True, teacher_id=teacher.id
    )
    q2 = Quiz(
        title='Entwurf', description='Test',
        is_published=False, teacher_id=teacher.id
    )
    session.add(q1)
    session.add(q2)
    session.commit()
    # Only the published quiz should be returned
    result = quiz_service.get_published(session)
    assert len(result) == 1
    assert result[0].title == 'Veroeffentlicht'
# TC_018 — publish sets is_published to True
def test_publish_sets_is_published(session):
    """TC_018: publish() should set is_published to True."""
    from domain.models import User, Quiz
    quiz_service = QuizService()
    # Create teacher and unpublished quiz
    teacher = User(
        username='l2', email='l2@t.ch',
        password_hash='hash', role='teacher'
    )
    session.add(teacher)
    session.commit()
    quiz = Quiz(
        title='Test Quiz', description='Test',
        is_published=False, teacher_id=teacher.id
    )
    session.add(quiz)
    session.commit()
    # Publish the quiz via service
    quiz_service.publish(session, quiz)
    # Verify it is now published
    result = session.get(Quiz, quiz.id)
    assert result.is_published == True