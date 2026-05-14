from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import Quiz


def teacher_dashboard(teacher_id: int):
    db = Database()
    session = db.get_session()
    quizze = session.exec(
        select(Quiz).where(Quiz.teacher_id == teacher_id)
    ).all()
    with ui.row().classes('w-full justify-between items-center mb-4'):
        ui.label('Meine Quizze').classes('text-2xl font-bold')
        ui.button(
            'Neues Quiz erstellen',
            on_click=lambda: ui.navigate.to('/teacher/create')
        )
    if not quizze:
        ui.label('Noch keine Quizze erstellt')
        return
    for quiz in quizze:
        with ui.card().classes('w-full mb-2'):
            with ui.row().classes('w-full justify-between'):
                with ui.column():
                    ui.label(quiz.title).classes('font-bold')
                    ui.label(quiz.description)
                with ui.column():
                    status = 'Veröffentlicht' if quiz.is_published else 'Entwurf'
                    ui.badge(status)
                    if not quiz.is_published:
                        ui.button(
                            'Veröffentlichen',
                            on_click=lambda q=quiz: publish_quiz(q, session)
                        )
                ui.button(
                    'Resultate',
                    on_click=lambda q=quiz:
                        ui.navigate.to(f'/teacher/results/{q.id}')
                )


def publish_quiz(quiz, session):
    quiz.is_published = True
    session.add(quiz)
    session.commit()
    ui.notify('Quiz veröffentlicht!', color='positive')
    ui.navigate.to('/teacher/dashboard')