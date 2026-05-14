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

    def submit_quiz():
        score = 0
        attempt = QuizAttempt(
            student_id=student_id,
            quiz_id=quiz_id,
            score=0,
            max_score=len(questions)
        )
        session.add(attempt)
        session.commit()

        for question in questions:
            sel_id = answers[question.id].value
            opt = session.get(AnswerOption, sel_id)
            ok = opt.is_correct if opt else False
            if ok:
                score += 1
            session.add(StudentAnswer(
                attempt_id=attempt.id,
                question_id=question.id,
                selected_answer_option_id=sel_id,
                is_correct=ok
            ))

        attempt.score = score
        session.add(attempt)
        session.commit()
        ui.navigate.to(f'/student/results/{attempt.id}')

    ui.button(
        'Quiz abgeben',
        on_click=submit_quiz
    ).classes('w-full mt-4')