from sqlalchemy import create_engine

#print(sqlalchemy.__version__)

DB_URI = 'postgresql://postgres:ClaveSimple123@localhost:5432/postgres'
engine = create_engine(DB_URI, echo=True)

try:
    connection = engine.connect()
    print('Connection successful')
    connection.close()
except Exception as e:
    print("Connection failed: ", e)