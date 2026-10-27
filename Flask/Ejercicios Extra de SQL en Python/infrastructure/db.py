import psycopg2, os, threading
from contextlib import contextmanager

class PgManager():
    def __init__(self, db_name, user, password, host, port=5432, min_conn=1, max_conn=10):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.min_conn = min_conn
        self.max_conn = max_conn
        self._depth = 0
        self._lock = threading.RLock()

        self.connection = self.create_connection(db_name, user, password, host, port)
        if self.connection:
            self.cursor = self.connection.cursor()
            print("Connected to database!")

    @classmethod
    def from_env(cls):
        return cls(
            db_name = os.environ["DB_NAME"],
            user = os.environ["DB_USER"],
            password = os.environ["DB_PASSWORD"],
            host = os.environ.get("DB_HOST","localhost"),
            port = int(os.environ.get("DB_PORT",5432)),
            min_conn = int(os.environ.get("DB_POOL_MIN",1)),
            max_conn = int(os.environ.get("DB_POOL_MAX",10))
        )

    @contextmanager
    def transaction(self):
        with self._lock:
            self._depth += 1
            try:
                yield
            except Exception:
                if self._depth == 1:
                    self.connection.rollback()
                raise
            else:
                if self._depth == 1:
                    self.connection.commit()
            finally:
                self._depth -= 1


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
        with self._lock:
            try:
                if params is None:
                    self.cursor.execute(query)
                else:
                    self.cursor.execute(query, params)

                if self._depth == 0:
                    self.connection.commit()

                if self.cursor.description:
                    return self.cursor.fetchall()
            except Exception as e:
                print("Error executing query:",e)
                if self._depth == 0:
                    self.connection.rollback()
                raise

    def ping(self):
        if not self.connection or self.connection.closed:
            return False
        try:
            result = self.execute_query("SELECT 1;") == [(1,)]
            return result
        except Exception:
            return False