from pydantic import BaseModel


class Genre(BaseModel):
    id: str
    name: str
    description: str | None


class GenresTransformer:
    def transform_genres(self, genres):
        transformed_genres = []
        for genre in genres:
            transformed_genre = Genre(id=genre['id'],
                                      name=genre['name'],
                                      description=genre['description'])

            transformed_genres.append(transformed_genre)

        return transformed_genres
