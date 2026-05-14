from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import Quiz, Question, AnswerOption
from domain.models import QuizAttempt, StudentAnswer


def quiz_view(quiz_id: int, student_id: int):
    db = Database()
    session = db.get_session()
    quiz = session.get(Quiz, quiz_id)
    questions = session.exec(
        select(Question).where(Question.quiz_id == quiz_id)
    ).all()

    ui.label(quiz.title).classes('text-2xl font-bold mb-4')
    answers = {}

    for question in questions:
        with ui.card().classes('w-full mb-4'):
            ui.label(question.text).classes('font-bold')
            options = session.exec(
                select(AnswerOption).where(
                    AnswerOption.question_id == question.id
                )
            ).all()
            selected = ui.radio(
                {opt.id: opt.text for opt in options},
                value=None
            )
            answers[question.id] = selected