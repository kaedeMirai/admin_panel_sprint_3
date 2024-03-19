from extract_tools.db_mixin import DatabaseMixin
from extract_tools.queries import QueryGenerator
from util.settings import retrieve_settings


class PersonsExtractor(DatabaseMixin):
    SETTINGS = retrieve_settings()
    SCHEMA = SETTINGS.db_schema

    def __init__(self, updated_at):
        super().__init__(self.SETTINGS)
        self.query_generator = QueryGenerator(self.SETTINGS.db_schema, updated_at)

    def execute_persons_query(self):
        query = self.query_generator.generate_persons_query()
        self._execute_query(query)

    def fetch_persons_records(self, records_amount=None):
        return self._fetch_records(records_amount)
