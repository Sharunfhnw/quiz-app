from nicegui import ui
from data_access.db import Database
from ui.pages import Pages


class QuizApplication:
    """App Kompositionswurzel — startet alles"""

    def __init__(self):
        self.database = Database()
        self.database.init_schema_and_seed()
        self.pages = Pages()

    def run(
        self,
        host: str = '0.0.0.0',
        port: int = 8080,
        reload: bool = False
    ) -> None:
        """NiceGUI App starten"""
        self.pages.register()
        ui.run(host=host, port=port, reload=reload)