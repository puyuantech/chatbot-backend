import re
import datetime
from elasticsearch import NotFoundError
from elasticsearch_dsl.query import Match, MatchPhrasePrefix, Terms, MultiMatch, Range, Term
from elasticsearch_dsl import Q


class Searcher:

    def __init__(self, conn, filters, doc_model):
        self.conn = conn
        self.filters = filters
        self.doc_model = doc_model

    def search_by_id(self, id):
        if self.doc_model is None:
            raise Exception('no doc model found')
        try:
            return self.doc_model.get(id)
        except NotFoundError as ex:
            return None
        except Exception as e:
            raise e

    def get_usually_query_result(self, key_word, offset, limit):
        return [], 0


class WXPublicAccountSearcher(Searcher):

    def get_usually_query_result(self, key_word, offset, limit, must_item=None):
        must, must_not, should, filters = [], [], [], []
        ss = self.doc_model.search()
        zh_model = re.compile(u'[a-z]')

        if zh_model.search(key_word):
            should.append(MatchPhrasePrefix(wx_name_pinyin=key_word))
            should.append(MatchPhrasePrefix(wx_name_first=key_word))
        else:
            should.append(Match(wx_name=key_word))

        should_match = 1  # if should else 0
        s = ss.query(Q(
            'bool',
            must=must,
            filter=filters,
            must_not=must_not,
            should=should,
            minimum_should_match=should_match
        ))

        _ = s[offset: offset + limit].execute()
        count = _.hits.total
        return _.hits, count


class WXArticleSearcher(Searcher):

    def get_usually_query_result(self, key_word, offset, limit, must_items=None, doc_ct_gt=None, doc_ct_lt=None):
        must, must_not, should, filters = [], [], [], []
        ss = self.doc_model.search()
        zh_model = re.compile(u'[a-z]')

        if key_word:
            if zh_model.search(key_word):
                should.append(MatchPhrasePrefix(article_title_pinyin=key_word))
                should.append(MatchPhrasePrefix(article_title_first=key_word))
            else:
                should.append(Match(article_title=key_word))

        if must_items:
            must.append(Terms(wxname=must_items))

        if doc_ct_gt:
            filters.append(Range(doc_ct={'gt': datetime.datetime.strptime(doc_ct_gt, '%Y-%m-%d')}))

        if doc_ct_lt:
            filters.append(Range(doc_ct={'lt': datetime.datetime.strptime(doc_ct_lt, '%Y-%m-%d')}))

        should_match = 0  # if should else 0
        s = ss.query(Q(
            'bool',
            must=must,
            filter=filters,
            must_not=must_not,
            should=should,
            minimum_should_match=should_match
        ))


        _ = s[offset: offset + limit].execute()
        count = _.hits.total
        return _.hits, count

