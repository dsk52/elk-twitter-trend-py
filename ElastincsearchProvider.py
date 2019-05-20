from elasticsearch import Elasticsearch


INDEX = "testindex"
DOC_TYPE = 'tweet'


class ElastincsearchProvider():
    def __init__(self):
        self.__es = Elasticsearch()

    def set(self, body):
        self.__es.index(index=INDEX, doc_type=DOC_TYPE, body=body)
