
from flask import request

from bases.viewhandler import ApiViewHandler
from utils.decorators import params_required
from extensions.es.es_conn import ElasticSearchConnector
from extensions.es.es_models import WeChatOASearchDoc, WeChatOAArticleSearchDoc
from extensions.es.es_searcher import WXPublicAccountSearcher, WXArticleSearcher


class WXPublicAccountAPI(ApiViewHandler):

    def get(self, key_word):
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('page_size', 5))
        offset = page * page_size

        conn = ElasticSearchConnector().get_conn()
        searcher = WXPublicAccountSearcher(conn, key_word, WeChatOASearchDoc)
        results, count = searcher.get_usually_query_result(key_word, offset, page_size)
        results = [[i.oa_id, i.wx_name] for i in results]

        return {
            'count': count.value,
            'page': page,
            'page_size': page_size,
            'results': results,
        }


class WXArticleAPI(ApiViewHandler):

    def get(self, key_word):
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('page_size', 5))
        offset = page * page_size

        conn = ElasticSearchConnector().get_conn()
        searcher = WXArticleSearcher(conn, key_word, WeChatOAArticleSearchDoc)
        results, count = searcher.get_usually_query_result(key_word, offset, page_size)
        results = [[i.article_id, i.article_title] for i in results]

        data = {
            'count': count.value,
            'page': page,
            'page_size': page_size,
            'results': results
        }
        print(data)

        return data
