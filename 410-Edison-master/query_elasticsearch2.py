# !/usr/bin/env python2
# -*- coding: utf-8 -*-

import elasticsearch

CONNECTION_TIMEOUT = 120
PAGE_SIZE = 100

ES_HOST = '192.99.62.203'
ES_PORT = '9201'
ES_INDEX = 'project-5bec7652be07770018d86cc4*'


class ElasticSearchHelper:
    _es_host = None
    _es_port = None
    _es_conn = None
    _use_ssl = False

    def __init__(self, es_host, es_port, use_ssl=False):
        self._es_host = es_host
        self._es_port = es_port
        self._use_ssl = use_ssl
        self.create_connection()

    def create_connection(self):
        es = elasticsearch.Elasticsearch([{'host': self._es_host, 'port': self._es_port}], timeout=CONNECTION_TIMEOUT,
                                         send_get_body_as='POST', use_ssl=self._use_ssl)
        es.cluster.health()
        self._es_conn = es

    def search(self, index, doc_type, search, scroll=None):
        if scroll:
            return self._es_conn.search(index=index, doc_type=doc_type, body=search, scroll=scroll)
        else:
            return self._es_conn.search(index=index, doc_type=doc_type, body=search)

    def scroll(self, scroll_id, scroll='1m'):
        return self._es_conn.scroll(scroll_id=scroll_id, scroll=scroll)


def format_results(results):
    """Print results nicely:
    doc_id) content
    """
    data = [doc for doc in results['hits']['hits']]
    for doc in data:
        print("%s) %s" % (doc['_id'], doc['_source']['text']))


def search(term,i, debug=False):
    """Simple Elasticsearch Query"""
    query = {
        "size": PAGE_SIZE,
        "query": {
            "match": {
                "text": term
            },
			"match": {
			    "office365EmailsIncludeMode":str(i)
			}
        }
    }
    es_helper = ElasticSearchHelper(ES_HOST, ES_PORT)
    response = es_helper.search(ES_INDEX, None, query, '2m')

    if debug:
        print("Printing the response below ::::")
        #f = open('resulting.json', 'w')
        #f.write(response)
        #f.close()
        print(response)
    return response


if __name__ == "__main__":
    term = "Frodo"
    res = search(term)
    format_results(res)
