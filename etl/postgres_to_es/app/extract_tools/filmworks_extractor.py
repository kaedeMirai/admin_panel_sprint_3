from extract_tools.db_mixin import DatabaseMixin
from extract_tools.queries import QueryGenerator
from util.settings import retrieve_settings


class FilmworksExtractor(DatabaseMixin):
    SETTINGS = retrieve_settings()
    SCHEMA = SETTINGS.db_schema
    PERSON_TABLE = 'person'
    GENRE_TABLE = 'genre'

    def __init__(self, updated_at):
        super().__init__(self.SETTINGS)
        self.query_generator = QueryGenerator(self.SETTINGS.db_schema, updated_at)

    def execute_filmworks_query(self):
        filmwork_ids = set()

        modified_person_ids = self._fetch_modified_record_ids_from_base_table(self.PERSON_TABLE)
        if modified_person_ids:
            formatted_person_ids = self._format_record_ids(modified_person_ids)
            person_filmwork_query = self.query_generator.generate_person_filmwork_query(formatted_person_ids)
            filmwork_ids.update(self._fetch_record_ids(person_filmwork_query))

        modified_genre_ids = self._fetch_modified_record_ids_from_base_table(self.GENRE_TABLE)
        if modified_genre_ids:
            formatted_genre_ids = self._format_record_ids(modified_genre_ids)
            genre_filmwork_query = self.query_generator.generate_genre_filmwork_query(formatted_genre_ids)
            filmwork_ids.update(self._fetch_record_ids(genre_filmwork_query))

        formatted_filmwork_ids = None
        if filmwork_ids:
            formatted_filmwork_ids = self._format_record_ids(filmwork_ids)

        query = self.query_generator.generate_full_filmwork_query(formatted_filmwork_ids)
        self._execute_query(query)

    def fetch_filmwork_records(self, records_amount=500):
        return self._fetch_records(records_amount)

    def _fetch_modified_record_ids_from_base_table(self, table_name):
        query = self.query_generator.generate_query_with_updated_at_field(table_name)
        record_ids = self._fetch_record_ids(query)

        return record_ids
