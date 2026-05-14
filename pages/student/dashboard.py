from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import Quiz


def student_dashboard():
    db = Database()
    session = db.get_session()

    ui.label('Verfuegbare Quizze').classes('text-2xl font-bold mb-4')
    quizze = session.exec(
        select(Quiz).where(Quiz.is_published == True)
    ).all()

    if not quizze:
        ui.label('Keine Quizze verfuegbar')
        return

    for quiz in quizze:
        with ui.card().classes('w-full mb-2'):
            ui.label(quiz.title).classes('font-bold')
            ui.label(quiz.description)
            ui.button(
                'Quiz starten',
                on_click=lambda q=quiz:
                    ui.navigate.to(f'/student/quiz/{q.id}')
            )