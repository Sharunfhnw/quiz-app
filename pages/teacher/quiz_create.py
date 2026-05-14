from nicegui import ui

from data_access.db import Database
from domain.models import AnswerOption, Question, Quiz


def quiz_create(teacher_id: int):
    db = Database()
    session = db.get_session()
    questions = []

    with ui.card().classes('w-full mb-4'):
        ui.label('Quiz Informationen').classes('font-bold mb-2')
        title = ui.input('Titel', placeholder='z.B. Mathematik Grundlagen')
        description = ui.input('Beschreibung', placeholder='Worum geht es?')

    with ui.card().classes('w-full mb-4'):
        ui.label('Fragen').classes('font-bold mb-2')
        ui.label('Noch keine Fragen hinzugefügt.')

    ui.button(
        'Quiz speichern',
        on_click=lambda: save_quiz(
            teacher_id=teacher_id,
            session=session,
            title=title.value,
            description=description.value,
            questions=questions,
        ),
    )


def save_quiz(teacher_id: int, session, title: str, description: str, questions: list):
    quiz = Quiz(
        title=title,
        description=description,
        teacher_id=teacher_id,
    )
    session.add(quiz)
    session.commit()
    ui.notify('Quiz gespeichert!', color='positive')
    ui.navigate.to('/teacher/dashboard')
