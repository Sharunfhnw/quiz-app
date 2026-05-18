"""Demo data seeder for LearnLoop.
Creates demo users and quizzes with all three question types
so the application can be tested immediately after setup.
Demo accounts:
    Teacher: lehrer / lehrer123
    Student: schueler / schueler123
"""
import hashlib
from sqlmodel import Session, select
from domain.models import User, Quiz, Question, AnswerOption
def hash_password(password: str) -> str:
    """Hash a password using SHA256.
    Args:
        password: Plain text password to hash.
    Returns:
        Hexadecimal SHA256 hash string.
    """
    return hashlib.sha256(password.encode()).hexdigest()
def seed_data(session: Session) -> None:
    """Insert demo data into the database if it is empty.
    Creates two demo users (teacher and student) and two quizzes
    with all three question types: single, multiple, truefalse.
    Args:
        session: Active database session.
    """
    # Check if data already exists — skip if so
    existing = session.exec(select(User)).first()
    if existing:
        return
    # Create demo teacher and student
    lehrer = User(
        username='lehrer',
        email='lehrer@learnloop.ch',
        password_hash=hash_password('lehrer123'),
        role='teacher'
    )
    schueler = User(
        username='schueler',
        email='schueler@learnloop.ch',
        password_hash=hash_password('schueler123'),
        role='student'
    )
    session.add(lehrer)
    session.add(schueler)
    session.commit()
    # Create Quiz 1: Mathematik with all 3 question types
    quiz1 = Quiz(
        title='Mathematik Grundlagen',
        description='Teste dein Wissen in Mathematik',
        is_published=True,
        teacher_id=lehrer.id
    )
    session.add(quiz1)
    session.commit()
    # Single Choice question — one correct answer
    f1 = Question(
        text='Was ist 2 + 2?',
        quiz_id=quiz1.id,
        question_type='single'
    )
    session.add(f1)
    session.commit()
    session.add_all([
        AnswerOption(text='3', is_correct=False, question_id=f1.id),
        AnswerOption(text='4', is_correct=True,  question_id=f1.id),
        AnswerOption(text='5', is_correct=False, question_id=f1.id),
        AnswerOption(text='6', is_correct=False, question_id=f1.id),
    ])
    session.commit()
    # True/False question — only Wahr/Falsch options
    f2 = Question(
        text='10 ist eine gerade Zahl.',
        quiz_id=quiz1.id,
        question_type='truefalse'
    )
    session.add(f2)
    session.commit()
    session.add_all([
        AnswerOption(text='Wahr',   is_correct=True,  question_id=f2.id),
        AnswerOption(text='Falsch', is_correct=False, question_id=f2.id),
    ])
    session.commit()
    # Multiple Choice question — multiple correct answers
    f3 = Question(
        text='Welche Zahlen sind Primzahlen?',
        quiz_id=quiz1.id,
        question_type='multiple'
    )
    session.add(f3)
    session.commit()
    session.add_all([
        AnswerOption(text='2', is_correct=True,  question_id=f3.id),
        AnswerOption(text='3', is_correct=True,  question_id=f3.id),
        AnswerOption(text='4', is_correct=False, question_id=f3.id),
        AnswerOption(text='7', is_correct=True,  question_id=f3.id),
    ])
    session.commit()
    print('LearnLoop demo data created!')
    print('  Teacher: lehrer / lehrer123')
    print('  Student: schueler / schueler123')