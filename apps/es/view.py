
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
        wx_name = request.args.get('wx_name')
        if wx_name:
            wx_name = wx_name.split(',')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('page_size', 5))
        offset = page * page_size

        conn = ElasticSearchConnector().get_conn()
        searcher = WXArticleSearcher(conn, key_word, WeChatOAArticleSearchDoc)
        results, count = searcher.get_usually_query_result(
            key_word, offset, page_size,
            must_items=wx_name,
            doc_ct_gt=start_date,
            doc_ct_lt=end_date,
        )
        results = [i.to_dict() for i in results]

        data = {
            'count': count.value,
            'page': page,
            'page_size': page_size,
            'results': results
        }
        return data
