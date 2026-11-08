import logging
import os
import threading
from contextlib import contextmanager

import psycopg2

logger = logging.getLogger(__name__)


class PgManager():
    def __init__(self, db_name, user, password, host, port=5432):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self._depth = 0
        self._lock = threading.RLock()

        self.connection = self.create_connection(db_name, user, password, host, port)
        logger.info("Connected to database.")

    @classmethod
    def from_env(cls):
        return cls(
            db_name = os.environ["DB_NAME"],
            user = os.environ["DB_USER"],
            password = os.environ["DB_PASSWORD"],
            host = os.environ.get("DB_HOST","localhost"),
            port = int(os.environ.get("DB_PORT",5432))
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
            return psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
        except Exception:
            logger.exception("Error connecting to database")
            raise

    def close_connection(self):
        if self.connection:
            self.connection.close()
        logger.info("Connection closed.")

    def execute_query(self, query, params=None):
        with self._lock:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, params)
                    results = cursor.fetchall() if cursor.description else None

                if self._depth == 0:
                    self.connection.commit()
                return results
            except Exception as e:
                logger.error("Error executing query: %s", e)
                if self._depth == 0:
                    self.connection.rollback()
                raise

    def ping(self):
        if not self.connection or self.connection.closed:
            return False
        try:
            return self.execute_query("SELECT 1;") == [(1,)]
        except Exception:
            return False
