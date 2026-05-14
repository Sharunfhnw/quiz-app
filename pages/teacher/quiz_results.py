from nicegui import ui
from sqlmodel import select

from data_access.db import Database
from domain.models import AnswerOption, Question, Quiz, QuizAttempt


def quiz_results(quiz_id: int):
    db = Database()
    session = db.get_session()

    quiz = session.get(Quiz, quiz_id)
    if not quiz:
        ui.label('Quiz nicht gefunden')
        return

    questions = session.exec(
        select(Question).where(Question.quiz_id == quiz_id)
    ).all()

    ui.label(quiz.title).classes('text-2xl font-bold mb-2')
    ui.label(quiz.description).classes('mb-4')

    attempts = session.exec(
        select(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id)
    ).all()

    if attempts:
        avg = sum(
            a.score / a.max_score * 100 for a in attempts
        ) / len(attempts)

        with ui.row().classes('gap-4 mb-4'):
            with ui.card():
                ui.label('Versuche').classes('text-sm')
                ui.label(str(len(attempts))).classes('text-2xl font-bold')
            with ui.card():
                ui.label('Durchschnitt').classes('text-sm')
                ui.label(f'{avg:.0f}%').classes('text-2xl font-bold')

    if not questions:
        ui.label('Für dieses Quiz sind noch keine Fragen vorhanden.')
        return

    for question in questions:
        options = session.exec(
            select(AnswerOption).where(AnswerOption.question_id == question.id)
        ).all()

        with ui.card().classes('w-full mb-3'):
            ui.label(question.text).classes('font-bold mb-2')
            for option in options:
                prefix = '✓' if option.is_correct else '•'
                ui.label(f'{prefix} {option.text}')
