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