import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from util.backoff import backoff
from util.settings import retrieve_settings

from load_tools.es_index_info import MOVIES_INDEX, MOVIES_INDEX_SETTINGS, MOVIES_INDEX_MAPPINGS
from load_tools.es_index_info import GENRES_INDEX, GENRES_INDEX_SETTINGS, GENRES_INDEX_MAPPINGS
from load_tools.es_index_info import PERSONS_INDEX, PERSONS_INDEX_SETTINGS, PERSONS_INDEX_MAPPINGS

import logging

logging.getLogger().setLevel(logging.INFO)


class EsLoader:
    settings = retrieve_settings()
    HOST = f'{settings.es_host}:{settings.es_port}'

    def __init__(self):
        self.client = Elasticsearch(self.HOST)

    def update_filmwork_docs(self, docs):
        index_info = self._build_index_info(MOVIES_INDEX, MOVIES_INDEX_SETTINGS, MOVIES_INDEX_MAPPINGS)
        self._update_docs(docs, index_info)

    def update_genre_docs(self, docs):
        index_info = self._build_index_info(GENRES_INDEX, GENRES_INDEX_SETTINGS, GENRES_INDEX_MAPPINGS)
        self._update_docs(docs, index_info)

    def update_person_docs(self, docs):
        index_info = self._build_index_info(PERSONS_INDEX, PERSONS_INDEX_SETTINGS, PERSONS_INDEX_MAPPINGS)
        self._update_docs(docs, index_info)

    def _update_docs(self, docs, index_info):
        self.create_index_if_not_exists(index_info)
        self.add_docs_to_index(docs, index_info['index'])

    @backoff(exceptions=(elasticsearch.ConnectionError,))
    def create_index_if_not_exists(self, index_info):
        is_index_exists = self.client.indices.exists(index=index_info['index'])

        if not is_index_exists:
            logging.info(f'Creating index {index_info["index"]}...')
            self.client.indices.create(index=index_info["index"],
                                       settings=index_info["settings"],
                                       mappings=index_info["mappings"])

    @backoff(exceptions=(elasticsearch.ConnectionError,))
    def add_docs_to_index(self, docs, index):
        logging.info(f'Adding {len(docs)} docs to {index} index...')
        actions = self._generate_update_actions(docs, index)
        helpers.bulk(self.client, actions)

    def _build_index_info(self, index, settings, mappings):
        return {
            'index': index,
            'settings': settings,
            'mappings': mappings
        }

    def _generate_update_actions(self, docs, index):
        actions = [
            {
                "_index": index,
                "_id": doc.id,
                "_source": doc.dict()
            }
            for doc in docs
        ]

        return actions
