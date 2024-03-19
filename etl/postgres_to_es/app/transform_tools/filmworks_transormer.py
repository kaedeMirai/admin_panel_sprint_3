from pydantic import BaseModel


class Person(BaseModel):
    id: str
    name: str


class Filmwork(BaseModel):
    id: str
    title: str | None
    description: str | None
    imdb_rating: float | None
    genre: list[str]
    director: list[str]
    writers_names: list[str]
    writers: list[Person]
    actors_names: list[str]
    actors: list[Person]


class FilmworkTransformer:
    def transform_filmworks(self, filmworks):
        converted_filmworks = []
        for filmwork in filmworks:
            director = self._build_director_object(filmwork)
            actors, actors_names = self._build_actors_data(filmwork)
            writers, writer_names = self._build_writers_data(filmwork)

            converted_filmwork = Filmwork(
                id=filmwork['id'],
                title=filmwork['title'],
                description=filmwork['description'],
                imdb_rating=filmwork['rating'],
                genre=filmwork['genres'],
                director=director,
                writers_names=writer_names,
                writers=writers,
                actors_names=actors_names,
                actors=actors,
            )
            converted_filmworks.append(converted_filmwork)

        return converted_filmworks

    @staticmethod
    def _build_director_object(filmwork):
        director = []
        for person in filmwork['persons']:
            if person['person_role'] == 'director':
                director.append(person['person_name'])

        return director

    @staticmethod
    def _build_actors_data(filmwork):
        actors = []
        actors_names = []
        for person in filmwork['persons']:
            if person['person_role'] == 'actor':
                actors_names.append(person['person_name'])
                actors.append(Person(
                    id=person['person_id'],
                    name=person['person_name']
                ))

        return actors, actors_names

    @staticmethod
    def _build_writers_data(filmwork):
        writers = []
        writers_names = []
        for person in filmwork['persons']:
            if person['person_role'] == 'writer':
                writers_names.append(person['person_name'])
                writers.append(Person(
                    id=person['person_id'],
                    name=person['person_name']
                ))

        return writers, writers_names
