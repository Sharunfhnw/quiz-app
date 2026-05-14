import hashlib
from nicegui import ui
from sqlmodel import select
from data_access.db import Database
from domain.models import User


def login_page():
    with ui.card().classes('w-96 mx-auto mt-20'):
        ui.label('Login').classes('text-2xl font-bold mb-4')
        username = ui.input('Benutzername')
        password = ui.input('Passwort', password=True)

        def do_login():
            if not username.value or not password.value:
                ui.notify('Alle Felder ausfullen!', color='negative')
                return
            db = Database()
            session = db.get_session()
            pw_hash = hashlib.sha256(
                password.value.encode()).hexdigest()
            user = session.exec(
                select(User).where(
                    User.username == username.value,
                    User.password_hash == pw_hash
                )
            ).first()
            if user and user.role == 'teacher':
                ui.navigate.to('/teacher/dashboard')
            elif user and user.role == 'student':
                ui.navigate.to('/student/dashboard')
            else:
                ui.notify('Login fehlgeschlagen!', color='negative')

        ui.button('Anmelden', on_click=do_login).classes('w-full')
        ui.link('Noch kein Konto? Registrieren', '/register')