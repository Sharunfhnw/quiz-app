from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import QuizAttempt, Quiz, StudentAnswer, Question, AnswerOption


def results_page(attempt_id: int):
    ui.query('body').style('background-color: #F8F7F4')

    db = Database()
    session = db.get_session()
    attempt = session.get(QuizAttempt, attempt_id)
    quiz = session.get(Quiz, attempt.quiz_id)
    pct = round(attempt.score / attempt.max_score * 100)

    # Header
    with ui.row().style(
        'width: 100%; background: white; padding: 12px 24px; '
        'align-items: center; justify-content: space-between; '
        'box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 24px'
    ):
        ui.button('← Zurück', on_click=lambda: ui.navigate.to('/student/dashboard')).style(
            'background: transparent; color: #666; font-size: 12px'
        )
        ui.label('Ergebnis').style(
            'font-size: 16px; font-weight: 500; color: #1A1A18'
        )
        ui.space()

    with ui.column().style('max-width: 700px; margin: 0 auto; padding: 0 20px'):

        # Score Karte
        with ui.card().style(
            'width: 100%; padding: 24px; border-radius: 10px; '
            'text-align: center; margin-bottom: 16px; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.06)'
        ):
            color = '#3B6D11' if pct >= 60 else '#A32D2D'
            ui.label(f'{pct}%').style(
                f'font-size: 48px; font-weight: 500; color: {color}'
            )
            ui.label(quiz.title).style(
                'font-size: 16px; font-weight: 500; margin-top: 8px'
            )
            if pct >= 90:
                msg = 'Ausgezeichnet! 🌟'
            elif pct >= 75:
                msg = 'Sehr gut! 👏'
            elif pct >= 60:
                msg = 'Gut gemacht! 👍'
            else:
                msg = 'Weiter üben! 💪'
            ui.label(msg).style('font-size: 14px; color: #666; margin-top: 4px')

            with ui.row().style('justify-content: center; gap: 16px; margin-top: 16px'):
                with ui.card().style('padding: 12px 20px; background: #EAF3DE'):
                    ui.label(str(attempt.score)).style('font-size: 20px; font-weight: 500; color: #3B6D11; text-align: center')
                    ui.label('Richtig').style('font-size: 11px; color: #666; text-align: center')
                with ui.card().style('padding: 12px 20px; background: #FCEBEB'):
                    ui.label(str(attempt.max_score - attempt.score)).style('font-size: 20px; font-weight: 500; color: #A32D2D; text-align: center')
                    ui.label('Falsch').style('font-size: 11px; color: #666; text-align: center')
                with ui.card().style('padding: 12px 20px; background: #F1EFE8'):
                    ui.label(str(attempt.max_score)).style('font-size: 20px; font-weight: 500; text-align: center')
                    ui.label('Gesamt').style('font-size: 11px; color: #666; text-align: center')

            with ui.row().style('gap: 8px; margin-top: 16px; justify-content: center'):
                ui.button('Dashboard', on_click=lambda: ui.navigate.to('/student/dashboard')).style(
                    'background-color: #3B6D11; color: white; border-radius: 8px; font-size: 12px'
                )
                ui.button('Nochmal', on_click=lambda: ui.navigate.to(f'/student/quiz/{attempt.quiz_id}')).style(
                    'background: transparent; border: 1px solid #ccc; border-radius: 8px; font-size: 12px'
                )

        # Detailauswertung
        with ui.card().style(
            'width: 100%; padding: 16px; border-radius: 10px; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.06)'
        ):
            ui.label('Detailauswertung').style(
                'font-size: 14px; font-weight: 500; margin-bottom: 12px'
            )

            sa_list = session.exec(
                select(StudentAnswer).where(
                    StudentAnswer.attempt_id == attempt_id
                )
            ).all()

            for sa in sa_list:
                q = session.get(Question, sa.question_id)
                opt = session.get(AnswerOption, sa.selected_answer_option_id)
                bg = '#EAF3DE' if sa.is_correct else '#FCEBEB'
                icon = '✓' if sa.is_correct else '✗'
                color = '#3B6D11' if sa.is_correct else '#A32D2D'
                with ui.row().style(
                    f'width: 100%; padding: 10px; margin-bottom: 6px; '
                    f'background: {bg}; border-radius: 8px; align-items: flex-start; gap: 10px'
                ):
                    ui.label(icon).style(f'color: {color}; font-weight: 500; font-size: 16px')
                    with ui.column():
                        ui.label(q.text).style('font-size: 13px; font-weight: 500')
                        ui.label(f'Deine Antwort: {opt.text}').style(f'font-size: 12px; color: {color}')