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


    
     # Demo-Quiz 1: Mathematik
    quiz1 = Quiz(
        title='Mathematik Grundlagen',
        description='Teste dein Wissen in Mathematik',
        is_published=True,
        teacher_id=lehrer.id
    )
    session.add(quiz1)
    session.commit()
    f1 = Question(text='Was ist 2 + 2?', quiz_id=quiz1.id)
    session.add(f1)
    session.commit()
    session.add_all([
        AnswerOption(text='3', is_correct=False, question_id=f1.id),
        AnswerOption(text='4', is_correct=True,  question_id=f1.id),
        AnswerOption(text='5', is_correct=False, question_id=f1.id),
        AnswerOption(text='6', is_correct=False, question_id=f1.id),
    ])
    session.commit()
    # Demo-Quiz 2: Englisch
    quiz2 = Quiz(
        title='Englisch Vokabeln',
        description='Wichtige englische Vokabeln',
        is_published=True,
        teacher_id=lehrer.id
    )
    session.add(quiz2)
    session.commit()
    f2 = Question(text="Was bedeutet 'apple'?", quiz_id=quiz2.id)
    session.add(f2)
    session.commit()
    session.add_all([
        AnswerOption(text='Birne', is_correct=False, question_id=f2.id),
        AnswerOption(text='Apfel', is_correct=True,  question_id=f2.id),
        AnswerOption(text='Orange',is_correct=False, question_id=f2.id),
        AnswerOption(text='Traube',is_correct=False, question_id=f2.id),
    ])
    session.commit()
    print('Demo-Quizze erstellt!')