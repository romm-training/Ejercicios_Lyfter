from sqlalchemy import insert, select

from db import engine, user_table

class UserRepository():
    def __init__(self, engine):
        self.engine = engine

    def create(self, username, password):
        stmt = (
            insert(user_table)
            .values(username=username, password=password)
            .returning(user_table.c.id)
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.first()

    def get_by_credentials(self, username, password):
        stmt = select(user_table).where(
            user_table.c.username == username,
            user_table.c.password == password
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.first()

    def get_by_id(self, user_id):
        stmt = select(user_table).where(
            user_table.c.id == user_id
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.first()

user_repository = UserRepository(engine)
