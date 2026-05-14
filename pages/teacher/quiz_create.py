from nicegui import ui

from data_access.db import Database
from domain.models import AnswerOption, Question, Quiz


def quiz_create(teacher_id: int):
    ui.query('body').style('background-color: #F8F7F4')
    db = Database()
    session = db.get_session()
    questions = []

    with ui.row().style(
        'width: 100%; background: white; padding: 12px 24px; '
        'align-items: center; justify-content: space-between; '
        'box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 24px'
    ):
        ui.button('← Zurück',
            on_click=lambda: ui.navigate.to('/teacher/dashboard')
        ).style('background: transparent; color: #666; font-size: 12px')
        ui.label('Neues Quiz erstellen').style(
            'font-size: 16px; font-weight: 500; color: #1A1A1B'
        )
        ui.space()

    with ui.column().style(
        'max-width: 700px; margin: 0 auto; padding: 0 20px'
    ):
        with ui.card().style(
            'width: 100%; padding: 16px; border-radius: 10px; '
            'margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06)'
        ):
            ui.label('Quiz Informationen').style(
                'font-size: 14px; font-weight: 500; margin-bottom: 10px'
            )
            title = ui.input('Titel').style('width: 100%')
            ui.space().style('height: 8px')
            description = ui.input('Beschreibung').style('width: 100%')

        with ui.card().style(
            'width: 100%; padding: 16px; border-radius: 10px; '
            'margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06)'
        ):
            ui.label('Frage hinzufuegen').style(
                'font-size: 14px; font-weight: 500; margin-bottom: 10px'
            )
            q_text = ui.input('Frage').style('width: 100%')
            ui.space().style('height: 8px')
            with ui.row().style('width: 100%; gap: 8px'):
                opt1 = ui.input('Option 1').style('flex: 1')
                opt2 = ui.input('Option 2').style('flex: 1')
            with ui.row().style('width: 100%; gap: 8px'):
                opt3 = ui.input('Option 3').style('flex: 1')
                opt4 = ui.input('Option 4').style('flex: 1')
            ui.space().style('height: 8px')
            correct = ui.select(
                label='Richtige Antwort',
                options=['Option 1','Option 2','Option 3','Option 4']
            ).style('width: 100%')
            q_list = ui.column()

        def add_question():
            if not q_text.value:
                ui.notify('Bitte Frage eingeben!', color='negative')
                return
            questions.append({
                'text': q_text.value,
                'options': [opt1.value, opt2.value,
                           opt3.value, opt4.value],
                'correct': correct.value
            })
            with q_list:
                ui.label(f'Frage {len(questions)}: {q_text.value}').style(
                    'font-size: 12px; color: #386D1; margin-top: 4px'
                )
            ui.notify('Frage hinzugefuegt', color='positive')
            q_text.value = opt1.value = opt2.value = ''
            opt3.value = opt4.value = ''

        ui.space().style('height: 8px')
        ui.button('Frage hinzufuegen', on_click=add_question).style(
            'background-color: #6B3FA0; color: white; '
            'border-radius: 8px; font-size: 12px'
        )

        def save_quiz():
            if not title.value:
                ui.notify('Titel erforderlich!', color='negative')
                return
            if not questions:
                ui.notify('Mind. 1 Frage erforderlich!', color='negative')
                return
            quiz = Quiz(title=title.value,
                       description=description.value,
                       teacher_id=teacher_id, is_published=False)
            session.add(quiz)
            session.commit()
            cm = {'Option 1':0,'Option 2':1,'Option 3':2,'Option 4':3}
            for q in questions:
                question = Question(text=q['text'], quiz_id=quiz.id)
                session.add(question)
                session.commit()
                for i, opt in enumerate(q['options']):
                    if not opt: continue
                    session.add(AnswerOption(
                        text=opt,
                        is_correct=(i == cm.get(q['correct'], -1)),
                        question_id=question.id
                    ))
                session.commit()
            ui.notify('Quiz gespeichert', color='positive')
            ui.navigate.to('/teacher/dashboard')

        ui.button('Quiz speichern', on_click=save_quiz).style(
            'width: 100%; background-color: #6B3FA0; color: white; '
            'border-radius: 8px; font-size: 13px; margin-top: 8px'
        )
