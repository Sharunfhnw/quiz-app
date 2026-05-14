from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import Quiz, Question, AnswerOption
from domain.models import QuizAttempt, StudentAnswer


def quiz_view(quiz_id: int, student_id: int):
    ui.query('body').style('background-color: #F8F7F4')

    db = Database()
    session = db.get_session()
    quiz = session.get(Quiz, quiz_id)
    questions = session.exec(
        select(Question).where(Question.quiz_id == quiz_id)
    ).all()

    # Header
    with ui.row().style(
        'width: 100%; background: white; padding: 12px 24px; '
        'align-items: center; justify-content: space-between; '
        'box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 24px'
    ):
        ui.button('← Zurück', on_click=lambda: ui.navigate.to('/student/dashboard')).style(
            'background: transparent; color: #666; font-size: 12px'
        )
        ui.label(quiz.title).style(
            'font-size: 16px; font-weight: 500; color: #1A1A18'
        )
        ui.label(f'{len(questions)} Fragen').style(
            'font-size: 12px; color: #666'
        )

    # Inhalt
    with ui.column().style('max-width: 700px; margin: 0 auto; padding: 0 20px'):
        answers = {}

        for i, question in enumerate(questions):
            with ui.card().style(
                'width: 100%; margin-bottom: 12px; padding: 16px; '
                'border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.06)'
            ):
                ui.label(f'Frage {i+1}: {question.text}').style(
                    'font-size: 14px; font-weight: 500; margin-bottom: 10px'
                )
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

        ui.button('Quiz abgeben', on_click=submit_quiz).style(
            'width: 100%; background-color: #3B6D11; color: white; '
            'border-radius: 8px; font-size: 13px; margin-top: 8px'
        )