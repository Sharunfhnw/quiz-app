from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import QuizAttempt, Quiz, StudentAnswer, Question, AnswerOption


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

    sa_list = session.exec(
        select(StudentAnswer).where(
            StudentAnswer.attempt_id == attempt_id
        )
    ).all()

    for sa in sa_list:
        q = session.get(Question, sa.question_id)
        opt = session.get(
            AnswerOption, sa.selected_answer_option_id
        )
        with ui.card().classes('w-full mb-1'):
            ui.label(q.text).classes('font-bold')
            color = 'text-green-600' if sa.is_correct \
                else 'text-red-600'
            ui.label(
                f'Deine Antwort: {opt.text}'
            ).classes(color)

    ui.button(
        'Zurueck zum Dashboard',
        on_click=lambda: ui.navigate.to('/student/dashboard')
    )