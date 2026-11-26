from db import PgManager

db_manager = PgManager(
    db_name="postgres",
    user="postgres",
    password="ClaveSimple123",
    host="localhost"
)

results = db_manager.execute_query(
    "INSERT INTO lyfter_duad.users (full_name, email, password) " \
    "VALUES (%s, %s, %s);", "John Doe", "john.doe@example.com", "securepassword"
)

print(results)

db_manager.close_connection()
