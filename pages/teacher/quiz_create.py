from nicegui import ui

from data_access.db import Database
from domain.models import AnswerOption, Question, Quiz


def quiz_create(teacher_id: int):
    db = Database()
    session = db.get_session()
    questions = []

    with ui.card().classes('w-full mb-4'):
        ui.label('Quiz Informationen').classes('font-bold mb-2')
        title = ui.input('Titel', placeholder='z.B. Mathematik Grundlagen')
        description = ui.input('Beschreibung', placeholder='Worum geht es?')

    with ui.card().classes('w-full mb-4'):
        ui.label('Fragen').classes('font-bold mb-2')
        ui.label('Noch keine Fragen hinzugefügt.')

    with ui.card().classes('w-full mb-4'):
        ui.label('Frage hinzufügen').classes('font-bold mb-2')
        q_text = ui.input('Frage')
        opt1 = ui.input('Option 1')
        opt2 = ui.input('Option 2')
        opt3 = ui.input('Option 3')
        opt4 = ui.input('Option 4')
        correct = ui.select(
            label='Richtige Antwort',
            options=['Option 1', 'Option 2', 'Option 3', 'Option 4'],
        )
        q_list = ui.column()

        def add_question():
            if not q_text.value:
                ui.notify('Bitte Frage eingeben!', color='negative')
                return
            questions.append({
                'text': q_text.value,
                'options': [opt1.value, opt2.value, opt3.value, opt4.value],
                'correct': correct.value,
            })
            with q_list:
                ui.label(f'Frage {len(questions)}: {q_text.value}')
            ui.notify('Frage hinzugefügt!', color='positive')
            q_text.value = opt1.value = opt2.value = ''
            opt3.value = opt4.value = ''

        ui.button('Frage hinzufügen', on_click=add_question)

    ui.button(
        'Quiz speichern',
        on_click=lambda: save_quiz(
            teacher_id=teacher_id,
            session=session,
            title=title.value,
            description=description.value,
            questions=questions,
        ),
    )


def save_quiz(teacher_id: int, session, title: str, description: str, questions: list):
    if not title:
        ui.notify('Titel erforderlich!', color='negative')
        return

    if not questions:
        ui.notify('Mind. 1 Frage erforderlich!', color='negative')
        return

    quiz = Quiz(
        title=title,
        description=description,
        teacher_id=teacher_id,
        is_published=False,
    )
    session.add(quiz)
    session.commit()

    correct_map = {
        'Option 1': 0, 'Option 2': 1, 'Option 3': 2, 'Option 4': 3
    }

    for q in questions:
        question = Question(text=q['text'], quiz_id=quiz.id)
        session.add(question)
        session.commit()

        for index, option in enumerate(q['options']):
            if not option:
                continue
            is_correct = index == correct_map.get(q['correct'], -1)
            session.add(AnswerOption(
                text=option,
                is_correct=is_correct,
                question_id=question.id,
            ))
        session.commit()

    ui.notify('Quiz gespeichert!', color='positive')
    ui.navigate.to('/teacher/dashboard')
