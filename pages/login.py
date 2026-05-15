import hashlib
from nicegui import ui, app
from sqlmodel import select
from data_access.db import Database
from domain.models import User


def login_page():
    ui.query('body').style('background-color: #F8F7F4')

    with ui.column().classes('absolute-center items-center'):
        ui.icon('school', size='48px').style('color: #185FA5')
        ui.label('Quiz Plattform').style(
            'font-size: 22px; font-weight: 500; color: #1A1A18; margin-top: 8px'
        )
        ui.label('Melde dich an um fortzufahren').style(
            'font-size: 13px; color: #666; margin-bottom: 16px'
        )

        with ui.card().style(
            'width: 340px; padding: 24px; border-radius: 12px; '
            'box-shadow: 0 1px 4px rgba(0,0,0,0.08)'
        ):
            username = ui.input('Benutzername').style('width: 100%')
            ui.space().style('height: 8px')
            password = ui.input('Passwort', password=True).style('width: 100%')
            ui.space().style('height: 12px')

            def do_login():
                if not username.value or not password.value:
                    ui.notify('Alle Felder ausfüllen!', color='negative')
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
                    app.storage.user['user_id'] = user.id
                    app.storage.user['username'] = user.username
                    app.storage.user['role'] = user.role
                    ui.navigate.to('/teacher/dashboard')
                elif user and user.role == 'student':
                    app.storage.user['user_id'] = user.id
                    app.storage.user['username'] = user.username
                    app.storage.user['role'] = user.role
                    ui.navigate.to('/student/dashboard')
                else:
                    ui.notify('Login fehlgeschlagen!', color='negative')

            ui.button('Anmelden', on_click=do_login).style(
                'width: 100%; background-color: #185FA5; color: white; '
                'border-radius: 8px; font-size: 13px'
            )
            ui.space().style('height: 8px')
            ui.link('Noch kein Konto? Registrieren', '/register').style(
                'font-size: 12px; color: #185FA5'
            )
            ui.separator()
            ui.label('Demo-Zugänge:').style(
                'font-size: 11px; font-weight: 500; color: #666; margin-top: 8px'
            )
            ui.label('Lehrer: lehrer / lehrer123').style(
                'font-size: 11px; color: #888'
            )
            ui.label('Schüler: schueler / schueler123').style(
                'font-size: 11px; color: #888'
            )