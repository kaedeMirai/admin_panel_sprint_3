import psycopg2
from psycopg2.extras import RealDictCursor

import logging

from util.backoff import backoff


class DatabaseMixin:
    DEFAULT_RECORDS_TO_FETCH_AMOUNT = 500

    def __init__(self, settings):
        self.dsl = self._build_dsl(settings)

        self.cursor = None
        self.conn = None

        try:
            self._connect()
        except (psycopg2.InterfaceError, psycopg2.OperationalError) as e:
            logging.error(e)
            raise InitialDatabaseConnectionException('Failed to establish initial connection to database')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def _connect(self):
        self.conn = psycopg2.connect(**self.dsl, cursor_factory=RealDictCursor, connect_timeout=5)
        self.cursor = self.conn.cursor()

    def _fetch_record_ids(self, query, records_amount=DEFAULT_RECORDS_TO_FETCH_AMOUNT):
        self._execute_query(query)

        record_ids = set()
        records = self._fetch_records(records_amount)
        while records:
            record_ids.update(self._extract_record_ids(records))
            records = self._fetch_records(records_amount)

        return record_ids

    @backoff(exceptions=(psycopg2.InterfaceError, psycopg2.OperationalError), start_sleep_time=1)
    def _execute_query(self, query):
        if not self.conn or self.conn.closed:
            self._connect()

        self.cursor.execute(query)

    @backoff(exceptions=(psycopg2.InterfaceError, psycopg2.OperationalError), start_sleep_time=1)
    def _fetch_records(self, records_amount=None):
        if not self.conn or self.conn.closed:
            self._connect()

        if records_amount:
            return self.cursor.fetchmany(records_amount)
        else:
            return self.cursor.fetchall()

    def _extract_record_ids(self, records):
        record_ids = set()
        for record in records:
            record_ids.add(record['id'])

        return record_ids

    def _format_record_ids(self, record_ids):
        formatted_ids = ', '.join("\'" + record_id + "\'" for record_id in record_ids)
        return formatted_ids

    def _build_dsl(self, settings):
        return {
            'dbname': settings.db_name,
            'user': settings.db_user,
            'password': settings.db_password,
            'host': settings.db_host,
            'port': settings.db_port
        }


class InitialDatabaseConnectionException(Exception):
    pass
