from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import Quiz


def student_dashboard():
    ui.query('body').style('background-color: #F8F7F4')

    # Header
    with ui.row().style(
        'width: 100%; background: white; padding: 12px 24px; '
        'align-items: center; justify-content: space-between; '
        'box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 24px'
    ):
        ui.label('📚 Schüler Dashboard').style(
            'font-size: 16px; font-weight: 500; color: #1A1A18'
        )
        ui.button('Abmelden', on_click=lambda: ui.navigate.to('/')).style(
            'background: transparent; color: #666; font-size: 12px'
        )

    # Inhalt
    with ui.column().style('max-width: 700px; margin: 0 auto; padding: 0 20px'):
        ui.label('Verfügbare Quizze').style(
            'font-size: 20px; font-weight: 500; margin-bottom: 16px'
        )

        db = Database()
        session = db.get_session()
        quizze = session.exec(
            select(Quiz).where(Quiz.is_published == True)
        ).all()

        if not quizze:
            ui.label('Keine Quizze verfügbar').style('color: #666')
            return

        for quiz in quizze:
            with ui.card().style(
                'width: 100%; margin-bottom: 10px; padding: 16px; '
                'border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.06)'
            ):
                with ui.row().style(
                    'width: 100%; justify-content: space-between; align-items: center'
                ):
                    with ui.column():
                        ui.label(quiz.title).style(
                            'font-size: 14px; font-weight: 500; color: #1A1A18'
                        )
                        ui.label(quiz.description).style(
                            'font-size: 12px; color: #666; margin-top: 2px'
                        )
                    ui.button(
                        'Starten',
                        on_click=lambda q=quiz: ui.navigate.to(f'/student/quiz/{q.id}')
                    ).style(
                        'background-color: #3B6D11; color: white; '
                        'border-radius: 8px; font-size: 12px'
                    )