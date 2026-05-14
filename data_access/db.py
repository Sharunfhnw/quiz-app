from sqlmodel import create_engine, SQLModel, Session
class Database:
    def __init__(self, url: str = 'sqlite:///quiz.db'):
        self.engine = create_engine(url)
    def init_schema_and_seed(self):
        from data_access.seed import seed_data
        SQLModel.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            seed_data(session)
    def get_session(self):
        return Session(self.engine)