import hashlib
from nicegui import ui
from data_access.db import Database
from domain.models import User


def register_page():
    with ui.card().classes('w-96 mx-auto mt-20'):
        ui.label('Registrieren').classes('text-2xl font-bold mb-4')
        username = ui.input('Benutzername')
        email = ui.input('E-Mail')
        password = ui.input('Passwort', password=True)
        role = ui.select(
            label='Rolle',
            options=['student', 'teacher']
        )

        def do_register():
            if not username.value or not password.value:
                ui.notify('Alle Felder ausfullen!', color='negative')
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

        ui.button('Registrieren', on_click=do_register).classes('w-full')
        ui.link('Bereits ein Konto? Login', '/')