class QueryGenerator:
    PERSON_TABLE = 'person'
    GENRE_TABLE = 'genre'
    FILMWORK_TABLE = 'film_work'
    PERSON_FILM_WORK_TABLE = 'person_film_work'
    GENRE_FILM_WORK_TABLE = 'genre_film_work'

    BASE_TABLE_FIELDS = ['id', 'updated_at']
    GENRE_TABLE_FIELDS = ['id', 'updated_at', 'name', 'description']
    PERSON_TABLE_FIELDS = ['id', 'updated_at', 'full_name']

    UPDATED_AT_FIELD = 'updated_at'

    def __init__(self, schema, updated_at):
        self.schema = schema
        self.updated_at = updated_at

    def generate_query_with_updated_at_field(self, table_name):
        fields = ', '.join(self.BASE_TABLE_FIELDS)
        query = f'SELECT {fields} ' \
                f'FROM {self.schema}.{table_name} ' \
                f'WHERE {self.UPDATED_AT_FIELD} > \'{self.updated_at}\';'

        return query

    def generate_genre_query(self):
        fields = ', '.join(self.GENRE_TABLE_FIELDS)
        query = f'SELECT {fields} ' \
                f'FROM {self.schema}.{self.GENRE_TABLE} ' \
                f'WHERE {self.UPDATED_AT_FIELD} > \'{self.updated_at}\';'

        return query

    def generate_persons_query(self):
        fields = ', '.join(self.PERSON_TABLE_FIELDS)
        query = f'SELECT {fields} ' \
                f'FROM {self.schema}.{self.PERSON_TABLE} ' \
                f'WHERE {self.UPDATED_AT_FIELD} > \'{self.updated_at}\';'

        return query

    def generate_full_filmwork_query(self, filmwork_ids):
        query = f'SELECT ' \
                f'fw.id as id, ' \
                f'fw.title, ' \
                f'fw.description, ' \
                f'fw.rating, ' \
                f'fw.type, ' \
                f'fw.created_at, ' \
                f'fw.updated_at, ' \
                f'COALESCE ( ' \
                f'    json_agg( ' \
                f'        DISTINCT jsonb_build_object( ' \
                f'            \'person_role\', pfw.role, ' \
                f'            \'person_id\', p.id, ' \
                f'            \'person_name\', p.full_name ' \
                f'         ) ' \
                f'    ) FILTER (WHERE p.id is not null), ' \
                f'    \'[]\' ' \
                f') as persons, ' \
                f'array_agg(DISTINCT g.name) as genres ' \
                f'FROM {self.schema}.{self.FILMWORK_TABLE} fw ' \
                f'LEFT JOIN {self.schema}.{self.PERSON_FILM_WORK_TABLE} pfw ON pfw.film_work_id = fw.id ' \
                f'LEFT JOIN {self.schema}.{self.PERSON_TABLE} p ON p.id = pfw.person_id ' \
                f'LEFT JOIN {self.schema}.{self.GENRE_FILM_WORK_TABLE} gfw ON gfw.film_work_id = fw.id ' \
                f'LEFT JOIN {self.schema}.{self.GENRE_TABLE} g ON g.id = gfw.genre_id '

        if filmwork_ids:
            query += f'WHERE fw.id IN ({filmwork_ids}) OR fw.{self.UPDATED_AT_FIELD} > \'{self.updated_at}\'' \
                     f'GROUP BY fw.id;'
        else:
            query += f'WHERE fw.{self.UPDATED_AT_FIELD} > \'{self.updated_at}\'' \
                     f'GROUP BY fw.id;'

        return query

    def generate_genre_filmwork_query(self, genre_ids):
        return f'SELECT fw.id, fw.updated_at ' \
               f'FROM {self.schema}.film_work fw ' \
               f'LEFT JOIN {self.schema}.genre_film_work gfw ON gfw.film_work_id = fw.id ' \
               f'WHERE gfw.genre_id IN ({genre_ids});'

    def generate_person_filmwork_query(self, person_ids):
        return f'SELECT fw.id, fw.updated_at ' \
               f'FROM {self.schema}.film_work fw ' \
               f'LEFT JOIN {self.schema}.person_film_work pfw ON pfw.film_work_id = fw.id ' \
               f'WHERE pfw.person_id IN ({person_ids})'
