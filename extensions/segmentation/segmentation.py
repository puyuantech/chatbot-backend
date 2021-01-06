import os
import json
import jieba

from bases.globals import settings
from utils.helper import Singleton


class Segmentation(metaclass=Singleton):

    def __init__(self):
        jieba.initialize()
        jieba.load_userdict(settings['USER_DICT_FILE'])

        with open(settings['FUND_COMPANY_LIST_FILE'], 'r') as f:
            self.fund_company_list = json.load(f)

        self.inverted_index = {}
        with open(settings['INVERTED_INDEX_FILE'], 'r') as f:
            inverted_index = json.load(f)

        for key, value in inverted_index.items():
            self.inverted_index[key] = set(value)

    def match(self, query):
        query_words = self._split_fund_name(query)

        candidates = set()
        for word in query_words:
            if word not in self.inverted_index:
                continue
            current_candidates = self.inverted_index[word]
            if not candidates:
                candidates = current_candidates
            else:
                candidates = candidates & current_candidates

        return candidates

    def _split_fund_name(self, query):
        result = []
        for company in self.fund_company_list:
            if query.startswith(company):
                result.append(company)
                query = query[len(company):]
                break

        seg_list = jieba.cut(query, cut_all=False)
        result.extend(seg_list)
        return result
