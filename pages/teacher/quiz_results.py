from nicegui import ui
from sqlmodel import select

from data_access.db import Database
from domain.models import QuizAttempt, User, Quiz


def quiz_results(quiz_id: int):
    ui.query('body').style('background-color: #F8F7F4')
    db = Database()
    session = db.get_session()
    quiz = session.get(Quiz, quiz_id)
    attempts = session.exec(
        select(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id)
    ).all()

    with ui.row().style(
        'width: 100%; background: white; padding: 12px 24px; '
        'align-items: center; justify-content: space-between; '
        'box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 24px'
    ):
        ui.button('← Zurück',
            on_click=lambda: ui.navigate.to('/teacher/dashboard')
        ).style('background: transparent; color: #666; font-size: 12px')
        ui.label(f'Resultate: {quiz.title}').style(
            'font-size: 16px; font-weight: 500; color: #1A1A1B'
        )
        ui.space()

    with ui.column().style(
        'max-width: 700px; margin: 0 auto; padding: 0 20px'
    ):
        if not attempts:
            ui.label('Noch keine Schüler').style('color: #666')
            return

        avg = sum(
            a.score / a.max_score * 100 for a in attempts
        ) / len(attempts)

        with ui.row().style('gap: 16px; margin-bottom: 16px; width: 100%'):
            with ui.card().style(
                'flex: 1; padding: 16px; border-radius: 10px; '
                'text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.06)'
            ):
                ui.label(str(len(attempts))).style(
                    'font-size: 24px; font-weight: 500'
                )
                ui.label('Versuche').style('font-size: 12px; color: #666')
            with ui.card().style(
                'flex: 1; padding: 16px; border-radius: 10px; '
                'text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.06)'
            ):
                ui.label(f'{avg:.0f}%').style(
                    'font-size: 24px; font-weight: 500; color: #3B6D11'
                )
                ui.label('Durchschnitt').style('font-size: 12px; color: #666')

        with ui.card().style(
            'width: 100%; padding: 16px; border-radius: 10px; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.06)'
        ):
            ui.label('Alle Schüler').style(
                'font-size: 14px; font-weight: 500; margin-bottom: 12px'
            )
            for attempt in attempts:
                student = session.get(User, attempt.student_id)
                pct = round(attempt.score / attempt.max_score * 100)
                color = '#3B6D11' if pct >= 60 else '#A32D2D'
                with ui.row().style(
                    'width: 100%; justify-content: space-between; '
                    'padding: 10px 0; border-bottom: 1px solid #F0F0F0'
                ):
                    ui.label(
                        student.username if student else '-'
                    ).style('font-size: 13px')
                    ui.label(
                        f'{attempt.score}/{attempt.max_score}'
                    ).style('font-size: 12px; color: #666')
                    ui.label(f'{pct}%').style(
                        f'font-size: 13px; font-weight: 500; color: {color}'
                    )
