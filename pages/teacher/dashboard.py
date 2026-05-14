from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import Quiz


def teacher_dashboard(teacher_id: int):
    ui.query('body').style('background-color: #F8F7F4')

    with ui.row().style(
        'width: 100%; background: white; padding: 12px 24px; '
        'align-items: center; justify-content: space-between; '
        'box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 24px'
    ):
        ui.label('Lehrer Dashboard').style(
            'font-size: 16px; font-weight: 500; color: #1A1A18'
        )
        with ui.row().style('gap: 8px'):
            ui.button(
                'Neues Quiz erstellen',
                on_click=lambda: ui.navigate.to('/teacher/create')
            ).style(
                'background-color: #6B3FA0; color: white; '
                'border-radius: 5px; font-size: 12px'
            )
            ui.button('Abmelden',
                on_click=lambda: ui.navigate.to('/')
            ).style(
                'background: transparent; color: #666; font-size: 12px'
            )

    with ui.column().style(
        'max-width: 700px; margin: 0 auto; padding: 0 20px'
    ):
        ui.label('Meine Quizze').style(
            'font-size: 20px; font-weight: 500; margin-bottom: 16px'
        )
        db = Database()
        session = db.get_session()
        quizze = session.exec(
            select(Quiz).where(Quiz.teacher_id == teacher_id)
        ).all()

        if not quizze:
            ui.label('Noch keine Quizze erstellt').style(
                'color: #999; font-size: 14px'
            )
            return

        for quiz in quizze:
            with ui.card().style(
                'width: 100%; margin-bottom: 16px; padding: 16px; '
                'border-radius: 8px; border: 1px solid #E5E3DC'
            ):
                with ui.row().style('width: 100%; gap: 12px; align-items: flex-start'):
                    with ui.column().style('flex: 1'):
                        ui.label(quiz.title).style(
                            'font-size: 16px; font-weight: 500; margin-bottom: 8px'
                        )
                        ui.label(quiz.description).style(
                            'font-size: 14px; color: #666; margin-bottom: 12px'
                        )
                        status = 'Veröffentlicht' if quiz.is_published else 'Entwurf'
                        ui.badge(status)
                    
                    with ui.column().style('gap: 8px'):
                        if not quiz.is_published:
                            ui.button(
                                'Veröffentlichen',
                                on_click=lambda q=quiz: publish_quiz(q, session)
                            ).style(
                                'background-color: #6B3FA0; color: white; '
                                'border-radius: 4px; font-size: 11px'
                            )
                        ui.button(
                            'Resultate',
                            on_click=lambda q=quiz:
                                ui.navigate.to(f'/teacher/results/{q.id}')
                        ).style(
                            'background-color: #E5E3DC; color: #333; '
                            'border-radius: 4px; font-size: 11px'
                        )


def publish_quiz(quiz, session):
    quiz.is_published = True
    session.add(quiz)
    session.commit()
    ui.notify('Quiz veröffentlicht!', color='positive')
    ui.navigate.to('/teacher/dashboard')