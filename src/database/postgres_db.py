import psycopg2
import psycopg2.extras
from psycopg2.sql import SQL, Identifier
from psycopg2._psycopg import AsIs

from src.utils.settings import Settings


class PostgresDb:
    def __init__(self):
        settings = Settings()
        db_settings = settings.get_database_settings()

        connection_parameters = ' '.join(['{}={}'.format(key, value) for (key, value) in db_settings.items()])
        self.connection = psycopg2.connect(connection_parameters)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


class PostgresDbTable:
    def __init__(self, table_name, schema='public'):
        self.db = PostgresDb()
        self.table_name = table_name
        self.schema = schema

    def get_dict(self, item_id):
        query = SQL('SELECT * FROM {}.{} WHERE id=%s;').format(
            Identifier(self.schema),
            Identifier(self.table_name))

        self.db.cursor.execute(query, [item_id])
        return self.db.cursor.fetchone()

    def exists(self, item_id):
        query = SQL('SELECT EXISTS(SELECT * FROM {}.{} WHERE id=%s);').format(
            Identifier(self.schema),
            Identifier(self.table_name))

        self.db.cursor.execute(query, [item_id])
        return self.db.cursor.fetchone()[0]

    def insert_dict(self, insertions):
        columns, values = zip(*insertions.items())

        query = SQL('INSERT INTO {}.{} (%s) VALUES %s').format(
            Identifier(self.schema),
            Identifier(self.table_name)
        )

        self.db.cursor.execute(query, [AsIs(','.join(columns)), values])
        self.db.connection.commit()

    def change_dict(self, item_id, changes):
        columns, values = zip(*changes.items())

        query = SQL('UPDATE {}.{} SET (%s) = %s WHERE id=%s').format(
            Identifier(self.schema),
            Identifier(self.table_name)
        )
        self.db.cursor.execute(query, [AsIs(','.join(columns)), values, item_id])
        self.db.connection.commit()


class PostgresDbConnection:
    def __init__(self):
        db_settings = Settings().get_database_settings()
        self._connection_parameters = ' '.join(['{}={}'.format(key, value) for (key, value) in db_settings.items()])

    def __enter__(self):
        self.connection = psycopg2.connect(self._connection_parameters)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class PostgresDbDictCursor(PostgresDbConnection):
    def __init__(self):
        super().__init__()

    def __enter__(self):
        super().__enter__()
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        super().__exit__(exc_type, exc_val, exc_tb)
