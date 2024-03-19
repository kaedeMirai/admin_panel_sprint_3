import time

from util.settings import retrieve_settings

from extract_tools.filmworks_extractor import FilmworksExtractor
from extract_tools.genres_extractor import GenresExtractor
from extract_tools.persons_extractor import PersonsExtractor

from load_tools.loader import EsLoader

from storage.storage_worker import JsonFileStorage, State

from transform_tools.filmworks_transormer import FilmworkTransformer
from transform_tools.genres_transformer import GenresTransformer
from transform_tools.persons_transformer import PersonsTransformer

from datetime import datetime


def run_data_transfer() -> None:
    storage = JsonFileStorage('storage/data/storage.json')
    state = State(storage)
    updated_at = state.get_state('updated_at')

    if not updated_at:
        settings = retrieve_settings()
        updated_at = settings.default_updated_at

    loader = EsLoader()

    run_filmworks_etl(updated_at, loader)
    run_genres_etl(updated_at, loader)
    run_persons_etl(updated_at, loader)

    state.set_state('updated_at', str(datetime.utcnow()))


def run_filmworks_etl(updated_at, loader):
    with FilmworksExtractor(updated_at) as extractor:
        extractor.execute_filmworks_query()

        filmwork_records = extractor.fetch_filmwork_records(500)
        while filmwork_records:
            transformed_records = FilmworkTransformer().transform_filmworks(filmwork_records)
            loader.update_filmwork_docs(transformed_records)
            filmwork_records = extractor.fetch_filmwork_records(500)


def run_genres_etl(updated_at, loader):
    with GenresExtractor(updated_at) as extractor:
        genres_records = extractor.fetch_genre_records()

        if genres_records:
            transformed_records = GenresTransformer().transform_genres(genres_records)
            loader.update_genre_docs(transformed_records)


def run_persons_etl(updated_at, loader):
    with PersonsExtractor(updated_at) as extractor:
        extractor.execute_persons_query()

        persons_records = extractor.fetch_persons_records(500)
        while persons_records:
            transformed_records = PersonsTransformer().transform_persons(persons_records)
            loader.update_person_docs(transformed_records)
            persons_records = extractor.fetch_persons_records(500)


if __name__ == '__main__':
    while True:
        run_data_transfer()
        time.sleep(15)
