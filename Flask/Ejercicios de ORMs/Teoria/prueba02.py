from sqlalchemy import text, engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT 'heelo world'"))
    print(result.all())

    users = conn.execute(text("SELECT * FROM users"))
    print(users.all())