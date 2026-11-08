from sqlalchemy import text, engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT 'hello world'"))
    print(result.all())

    users = conn.execute(text("SELECT * FROM users"))
    print(users.all())