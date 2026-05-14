from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import QuizAttempt, Quiz


def results_page(attempt_id: int):
    db = Database()
    session = db.get_session()
    attempt = session.get(QuizAttempt, attempt_id)
    quiz = session.get(Quiz, attempt.quiz_id)
    pct = round(attempt.score / attempt.max_score * 100)

    with ui.card().classes('w-full text-center mb-4'):
        ui.label(quiz.title).classes('text-2xl font-bold')
        ui.label(
            f'{attempt.score}/{attempt.max_score} = {pct}%'
        ).classes('text-xl')

        if pct >= 90:
            msg = 'Ausgezeichnet! 🌟'
        elif pct >= 75:
            msg = 'Sehr gut! 👏'
        elif pct >= 60:
            msg = 'Gut gemacht! 👍'
        else:
            msg = 'Weiter ueben! 💪'
        ui.label(msg)

    ui.button(
        'Zurueck zum Dashboard',
        on_click=lambda: ui.navigate.to('/student/dashboard')
    )