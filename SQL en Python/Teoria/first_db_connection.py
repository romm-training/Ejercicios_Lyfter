import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="ClaveSimple123",
    dbname="postgres"
)

print("Connected to the database")

cursor = connection.cursor()

cursor.execute("SELECT id, full_name, email, password FROM lyfter_duad.users;")
print("Query executed")

def format_user(user_record):
    return {
        "id": user_record[0],
        "full_name": user_record[1],
        "email": user_record[2],
        "password": user_record[3]
    }

results = cursor.fetchall()
formatted_results = [format_user(user) for user in results]
print(formatted_results)

cursor.execute(
    "INSERT INTO lyfter_duad.users (full_name, email, password) " \
    "VALUES ('Juan Jose Restrepo', 'juan.jo@mail.com', '12345');"
)
print("Insert executed")

connection.commit()
print("Connection changes committed")
