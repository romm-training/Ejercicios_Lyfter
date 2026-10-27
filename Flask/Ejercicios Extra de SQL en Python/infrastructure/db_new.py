import logging
import os
from contextlib import contextmanager

from psycopg2 import pool
from psycopg2.pool import PoolError

logger = logging.getLogger(__name__)


class DatabaseUnavailableError(Exception):
    """No hay conexiones libres en el pool (routes lo traduce a HTTP 503)."""


def _execute(connection, query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if cursor.description:
            return cursor.fetchall()
        return None


class Transaction:
    """Conexión propia de una transacción. No hace commit ni rollback: lo hace db.transaction()."""

    def __init__(self, connection):
        self._connection = connection

    def execute_query(self, query, params=None):
        return _execute(self._connection, query, params)


class PgManager():
    def __init__(self, db_name, user, password, host, port=5432, minconn=1, maxconn=10):
        self.pool = pool.ThreadedConnectionPool(
            minconn,
            maxconn,
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        logger.info("Pool de conexiones creado (min=%s, max=%s).", minconn, maxconn)

    @classmethod
    def from_env(cls):
        # load_dotenv() se llama antes, en app.py
        return cls(
            db_name=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ.get("DB_PORT", 5432)),
            minconn=int(os.environ.get("DB_POOL_MIN", 1)),
            maxconn=int(os.environ.get("DB_POOL_MAX", 10))
        )

    def _get_connection(self):
        try:
            return self.pool.getconn()
        except PoolError as e:
            raise DatabaseUnavailableError("No hay conexiones disponibles en el pool.") from e

    def _release(self, connection):
        # Si la conexión quedó rota, se descarta en vez de devolverla al pool
        self.pool.putconn(connection, close=bool(connection.closed))

    def execute_query(self, query, params=None):
        """Consulta única con commit propio. Para operaciones de varias consultas usar transaction()."""
        connection = self._get_connection()
        try:
            results = _execute(connection, query, params)
            connection.commit()
            return results
        except Exception as e:
            logger.error("Error executing query: %s", e)
            connection.rollback()
            raise
        finally:
            self._release(connection)

    @contextmanager
    def transaction(self):
        """Entrega un Transaction; commit al salir bien, rollback si hay excepción."""
        connection = self._get_connection()
        try:
            yield Transaction(connection)
            connection.commit()
        except Exception as e:
            logger.error("Transaction rolled back: %s", e)
            connection.rollback()
            raise
        finally:
            self._release(connection)

    def close_connection(self):
        self.pool.closeall()
        logger.info("Pool de conexiones cerrado.")
