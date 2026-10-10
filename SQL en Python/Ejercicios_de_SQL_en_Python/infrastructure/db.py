import psycopg2

class PgManager():
    def __init__(self, db_name, user, password, host, port=5432):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.connection = self.create_connection(db_name, user, password, host, port)
        if self.connection:
            self.cursor = self.connection.cursor()
            print("Connected to database!")

    def create_connection(self, db_name, user, password, host, port):
        try:
            connection = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            return connection
        except Exception as e:
            print("Error connecting to database:", e)
            return None

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")

    def execute_query(self, query, params=None):
        try:
            if params is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, params)
            self.connection.commit()

            if self.cursor.description:
                results = self.cursor.fetchall()
                return results
        except Exception as e:
            print("Error executing query:", e)
            self.connection.rollback()
            raise
