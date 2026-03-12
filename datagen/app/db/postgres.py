import psycopg2
from psycopg2.extras import execute_values
from app.models import Install, Action

class PostgresClient:
    def __init__(self, config):
        self.config = config
        self.conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            dbname=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            options=f"-c search_path={config.POSTGRES_SCHEMA}"
        )
        self.conn.autocommit = True

    def create_tables(self):
        pass

    def clear_all(self):
        with self.conn.cursor() as cur:
            cur.execute('TRUNCATE installs, fct_actions RESTART IDENTITY CASCADE')

    def insert_installs(self, installs: list[Install]):
        if not installs:
            return
        data = [i.as_tuple() for i in installs]
        with self.conn.cursor() as cur:
            execute_values(cur, '''
                INSERT INTO installs (user_id, install_timestamp, source)
                VALUES %s
            ''', data)

    def insert_actions(self, actions: list[Action]):
        if not actions:
            return
        data = [a.as_tuple() for a in actions]
        with self.conn.cursor() as cur:
            execute_values(cur, '''
                INSERT INTO fct_actions (user_id, session_start, actions)
                VALUES %s
            ''', data)
