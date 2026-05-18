"""Database connection and schema management for LearnLoop.
Provides the Database class which handles:- SQLite engine creation- Schema initialization (creates all tables)- Demo data seeding- Session management for database operations
"""
from sqlmodel import SQLModel, create_engine, Session
from data_access.seed import seed_data
class Database:
    """Manages the SQLite database connection for LearnLoop.
    Uses SQLModel (built on SQLAlchemy) as the ORM layer.
    All database operations go through a Session object.
    Example:
        db = Database()
        session = db.get_session()
        users = session.exec(select(User)).all()
    """
    # SQLite database file stored in the project root
    DATABASE_URL = 'sqlite:///quiz.db'
    def __init__(self):
        """Initialize the database engine."""
        # Create SQLite engine (connect_args avoids threading issues)
        self.engine = create_engine(
            self.DATABASE_URL,
            connect_args={'check_same_thread': False}
        )
    def init_schema_and_seed(self) -> None:
        """Create all database tables and insert demo data.
        Called once at application startup.
        If the database already has data, seeding is skipped.
        """
        # Create all tables defined in domain/models.py
        SQLModel.metadata.create_all(self.engine)
        # Insert demo users and quizzes if DB is empty
        with Session(self.engine) as session:
            seed_data(session)
    def get_session(self) -> Session:
        """Create and return a new database session.
        A Session is a temporary connection to the database.
        Think of it like a shopping cart:
        - session.add()    = add item to cart
        - session.commit() = checkout (saves to DB)
        Returns:
            A new SQLModel Session object.
        """
        return Session(self.engine)