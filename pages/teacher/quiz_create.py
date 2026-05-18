from nicegui import ui

from data_access.db import Database
from services.quiz_service import QuizService


def quiz_create(teacher_id: int):
	ui.query('body').style('background-color:#F5F5F7;margin:0')
	db = Database()
	session = db.get_session()
	quiz_service = QuizService()
	questions = []

	# Top bar
	with ui.row().style(
		'width:100%;background:white;padding:16px 24px;'
		'align-items:center;gap:12px;'
		'border-bottom:0.5px solid #E5E5E5;margin-bottom:24px'
	):
		ui.button('← Zurueck', on_click=lambda: ui.navigate.to('/teacher/dashboard')).style('font-size:12px')
		ui.label('Neues Quiz erstellen').style('font-size:16px;font-weight:500')

	with ui.row().style('padding:0 24px 24px;gap:16px;align-items:flex-start'):
		with ui.column().style('flex:1;gap:12px'):
			# Quiz information
			with ui.card().style('padding:20px;border-radius:12px'):
				ui.label('Quiz Informationen').style('font-size:14px;font-weight:500;margin-bottom:14px')
				ui.label('Titel').style('font-size:13px;font-weight:500;margin-bottom:6px')
				title = ui.input(placeholder='z.B. Mathematik Grundlagen').style('width:100%')
				ui.label('Beschreibung').style('font-size:13px;font-weight:500;margin-bottom:6px;margin-top:10px')
				description = ui.input(placeholder='Worum geht es?').style('width:100%')

			# Add question
			with ui.card().style('padding:20px;border-radius:12px'):
				ui.label('Frage hinzufuegen').style('font-size:14px;font-weight:500;margin-bottom:14px')
				# Question type
				ui.label('Fragetyp').style('font-size:13px;font-weight:500;margin-bottom:6px')
				q_type = ui.select(
					options={
						'single': 'Single Choice',
						'multiple': 'Multiple Choice',
						'truefalse': 'Wahr/Falsch'
					},
					value='single'
				).style('width:100%')

				# Question text
				ui.label('Frage').style('font-size:13px;font-weight:500;margin-bottom:6px;margin-top:10px')
				q_text = ui.input(placeholder='Deine Frage hier...').style('width:100%')

				# Options container (hidden for True/False)
				opts_container = ui.column().style('width:100%;margin-top:10px')
				with opts_container:
					ui.label('Antwortoptionen').style('font-size:13px;font-weight:500;margin-bottom:6px')
					with ui.row().style('gap:8px;width:100%'):
						opt1 = ui.input('Option 1').style('flex:1')
						opt2 = ui.input('Option 2').style('flex:1')
					with ui.row().style('gap:8px;width:100%;margin-top:8px'):
						opt3 = ui.input('Option 3').style('flex:1')
						opt4 = ui.input('Option 4').style('flex:1')

				# Single choice — a dropdown
				single_area = ui.column().style('width:100%;margin-top:10px')
				with single_area:
					ui.label('Richtige Antwort').style('font-size:13px;font-weight:500;margin-bottom:6px')
					correct_single = ui.select(options=['Option 1', 'Option 2', 'Option 3', 'Option 4']).style('width:100%')

				# Multiple choice — checkboxes
				multi_area = ui.column().style('width:100%;margin-top:10px;display:none')
				with multi_area:
					ui.label('Richtige Antworten (mehrere moeglich)').style('font-size:13px;font-weight:500;margin-bottom:6px')
					cb1 = ui.checkbox('Option 1 ist korrekt')
					cb2 = ui.checkbox('Option 2 ist korrekt')
					cb3 = ui.checkbox('Option 3 ist korrekt')
					cb4 = ui.checkbox('Option 4 ist korrekt')

				# Question type switch — show/hide sections
				def on_type_change(val):
					if val == 'truefalse':
						opts_container.style('display:none')
						single_area.style('display:none')
						multi_area.style('display:none')
					elif val == 'multiple':
						opts_container.style('display:block')
						single_area.style('display:none')
						multi_area.style('display:block')
					else:  # single
						opts_container.style('display:block')
						single_area.style('display:block')
						multi_area.style('display:none')

				q_type.on_value_change(lambda e: on_type_change(e.value))

				q_list = ui.column()

				def add_question():
					if not q_text.value:
						ui.notify('Bitte Frage eingeben!', color='negative')
						return
					tl = {
						'single': 'SC',
						'multiple': 'MC',
						'truefalse': 'T/F'
					}
					# Collect correct answers depending on type
					if q_type.value == 'multiple':
						correct_list = []
						if cb1.value:
							correct_list.append(0)
						if cb2.value:
							correct_list.append(1)
						if cb3.value:
							correct_list.append(2)
						if cb4.value:
							correct_list.append(3)
						if not correct_list:
							ui.notify('Mind. eine richtige Antwort!', color='negative')
							return
					elif q_type.value == 'single':
						cm = {'Option 1': 0, 'Option 2': 1, 'Option 3': 2, 'Option 4': 3}
						correct_list = [cm.get(correct_single.value, -1)]
					else:
						correct_list = []

					questions.append({
						'text': q_text.value,
						'type': q_type.value,
						'options': [opt1.value, opt2.value, opt3.value, opt4.value],
						'correct_list': correct_list
					})
					with q_list:
						ui.label(f"[{tl.get(q_type.value,'')}] {q_text.value}").style('font-size:12px;color:#3B6D11;margin-top:4px')
					ui.notify('Frage hinzugefuegt!', color='positive')
					q_text.value = ''
					opt1.value = opt2.value = ''
					opt3.value = opt4.value = ''
					cb1.value = cb2.value = False
					cb3.value = cb4.value = False

				ui.button('+ Frage hinzufuegen', on_click=add_question).style('background:#111;color:white;border-radius:8px;font-size:12px;margin-top:12px;width:100%')

		# Right side — question list and save
		with ui.card().style('width:300px;padding:20px;border-radius:12px'):
			ui.label('Fragen (0)').style('font-size:14px;font-weight:500;margin-bottom:4px')
			ui.label('Ihre hinzugefuegten Fragen').style('font-size:12px;color:#666;margin-bottom:16px')
			q_display = ui.column()
			ui.html('<hr style="border:none;border-top:0.5px solid #E5E5E5;margin:12px 0">')

			def save_quiz():
				if not title.value:
					ui.notify('Titel erforderlich!', color='negative')
					return
				if not questions:
					ui.notify('Mind. 1 Frage!', color='negative')
					return
				# Create quiz via service
				quiz = quiz_service.create(session=session, title=title.value, description=description.value, teacher_id=teacher_id)
				# Save questions and answers
				for q in questions:
					question = quiz_service.add_question(session=session, text=q['text'], quiz_id=quiz.id, question_type=q['type'])
					if q['type'] == 'truefalse':
						quiz_service.add_answer_option(session, 'Wahr', True, question.id)
						quiz_service.add_answer_option(session, 'Falsch', False, question.id)
					else:
						for i, opt in enumerate(q['options']):
							if not opt:
								continue
							is_correct = i in q['correct_list']
							quiz_service.add_answer_option(session, opt, is_correct, question.id)
				ui.notify('Quiz gespeichert!', color='positive')
				ui.navigate.to('/teacher/dashboard')

			ui.button('Quiz speichern', on_click=save_quiz).style('background:#111;color:white;border-radius:8px;font-size:13px;width:100%')
