from extract_tools.db_mixin import DatabaseMixin
from extract_tools.queries import QueryGenerator
from util.settings import retrieve_settings


class GenresExtractor(DatabaseMixin):
    SETTINGS = retrieve_settings()
    SCHEMA = SETTINGS.db_schema

    def __init__(self, updated_at):
        super().__init__(self.SETTINGS)
        self.query_generator = QueryGenerator(self.SETTINGS.db_schema, updated_at)

    def fetch_genre_records(self):
        query = self.query_generator.generate_genre_query()
        self._execute_query(query)

        return self._fetch_records()
