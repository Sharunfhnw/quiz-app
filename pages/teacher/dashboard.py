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
            ui.label('Noch keine Quizze erstellt').style('color: #666')
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
                        sc = '#2AF3DE' if quiz.is_published else '#F1EF8'
                        tc = '#3B6D1' if quiz.is_published else '#444441'
                        st = 'Veröffentlicht' if quiz.is_published else 'Entwurf'
                        ui.label(st).style(
                            f'font-size: 11px; font-weight: 500; '
                            f'background: {sc}; color: {tc}; '
                            f'padding: 2px 8px; border-radius: 20px; margin-top: 6px'
                        )
                    with ui.column().style('gap: 6px; align-items: flex-end'):
                        if not quiz.is_published:
                            def publish(q=quiz):
                                q.is_published = True
                                session.add(q)
                                session.commit()
                                ui.notify('Quiz veröffentlicht!', color='positive')
                                ui.navigate.to('/teacher/dashboard')
                            ui.button('Veröffentlichen',
                                on_click=publish
                            ).style(
                                'background-color: #6B3FA0; color: white; '
                                'border-radius: 5px; font-size: 12px'
                            )
                        ui.button('Resultate',
                            on_click=lambda q=quiz:
                                ui.navigate.to(f'/teacher/results/{q.id}')
                        ).style(
                            'background: transparent; border: 1px solid #ccc; '
                            'border-radius: 5px; font-size: 12px'
                        )