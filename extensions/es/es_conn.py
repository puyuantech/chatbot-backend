from utils.helper import Singleton
from bases.globals import settings
from elasticsearch_dsl.connections import connections


class ElasticSearchConnector(metaclass=Singleton):

    def __init__(self):
        conf = settings['ES']['es_test']
        self.conn = connections.create_connection(
            hosts=conf['hosts'],
            http_auth=(conf['username'], conf['password']),
        )

    def get_conn(self):
        return self.conn

