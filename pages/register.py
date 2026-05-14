import hashlib
from nicegui import ui
from data_access.db import Database
from domain.models import User


def register_page():
    ui.query('body').style('background-color: #F8F7F4')

    with ui.column().classes('absolute-center items-center'):
        ui.icon('school', size='48px').style('color: #185FA5')
        ui.label('Quiz Plattform').style(
            'font-size: 22px; font-weight: 500; color: #1A1A18; margin-top: 8px'
        )
        ui.label('Erstelle dein Konto').style(
            'font-size: 13px; color: #666; margin-bottom: 16px'
        )

        with ui.card().style(
            'width: 340px; padding: 24px; border-radius: 12px; '
            'box-shadow: 0 1px 4px rgba(0,0,0,0.08)'
        ):
            username = ui.input('Benutzername').style('width: 100%')
            ui.space().style('height: 8px')
            email = ui.input('E-Mail').style('width: 100%')
            ui.space().style('height: 8px')
            password = ui.input('Passwort', password=True).style('width: 100%')
            ui.space().style('height: 8px')
            role = ui.select(
                label='Rolle',
                options=['student', 'teacher']
            ).style('width: 100%')
            ui.space().style('height: 12px')

            def do_register():
                if not username.value or not password.value:
                    ui.notify('Alle Felder ausfüllen!', color='negative')
                    return
                if len(password.value) < 6:
                    ui.notify('Passwort mind. 6 Zeichen!', color='negative')
                    return
                db = Database()
                session = db.get_session()
                new_user = User(
                    username=username.value,
                    email=email.value,
                    password_hash=hashlib.sha256(
                        password.value.encode()).hexdigest(),
                    role=role.value or 'student'
                )
                session.add(new_user)
                session.commit()
                ui.notify('Konto erstellt!', color='positive')
                ui.navigate.to('/')

            ui.button('Registrieren', on_click=do_register).style(
                'width: 100%; background-color: #185FA5; color: white; '
                'border-radius: 8px; font-size: 13px'
            )
            ui.space().style('height: 8px')
            ui.link('Bereits ein Konto? Login', '/').style(
                'font-size: 12px; color: #185FA5'
            )