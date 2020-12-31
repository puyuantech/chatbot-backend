from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Float, Nested
from robo.utils.es.es_models import FundSearchDoc, IndexSearchDoc, StrategySearchDoc

conn = connections.create_connection(hosts=['39.98.109.26:9200'], http_auth=('elastic', '7QspOCSeKjeKrzyaFvc0'))

# conn.count()

# 获取索引  * 取所有
indices = conn.indices.get('*')
for i in indices:
    print(i)

# print(StrategySearchDoc.get(1).to_dict())

class StockPledgeeDetailDoc(Document):
    stock_code = Text(analyzer='ik_max_word')
    company_name = Text(analyzer='ik_max_word')
    pledgee = Text(analyzer='pinyin')
    pledgee_index = Text(analyzer='ik_max_word')
    pledgee_first = Text(analyzer='standard')
    institution_type = Text(analyzer='whitespace')
    pledge_number = Float()
    create_time = Date()

    class Index:
        name = 'stock_pledgee_detail'

    def save(self, **kwargs):
        return super(StockPledgeeDetailDoc, self).save(**kwargs)
# for i in range(91, 101):
#     a = StrategySearchDoc.get(i)
#     a.delete(ignore=[400, 404])
#     print(a)
# get by id
# print(StockPledgeeDetailDoc.get('VUx3XnIBFEZmxo-6kkNQ').to_dict())

# 删除
# conn.indices.delete('fund_search_v2')
# conn.indices.delete('fund_search_v3')
# conn.indices.delete('index_search_v1')
# conn.indices.delete('strategy_search_v1')




# 创建
# StockPledgeeDetailDoc.init()


# 插入数据
# from surfing.data.api.view import ViewDataApi
# from robo.config import robo_configurator
# fund_df = ViewDataApi().get_fund_daily_collection()
# """
#             基金ID    datetime     基金代码  ...  基金类别 基金评分        _update_time
# 0       000001!0  2020-05-28   000001  ...  None  NaN 2020-05-28 16:17:05
# 1       000003!0  2020-05-28   000003  ...  None  NaN 2020-05-28 16:17:05
# """
# from robo.utils.es.es_tools import build_pinyin
# for i in fund_df.index:
#     new_s = StockPledgeeDetailDoc(
#         stock_code=fund_df.loc[i, '基金代码'],
#         company_name=fund_df.loc[i, '基金名称'],
#         pledgee=fund_df.loc[i, '基金名称'],
#         pledgee_index=fund_df.loc[i, '基金名称'],
#         pledgee_first=build_pinyin(fund_df.loc[i, '基金名称']),
#     )
#     new_s.save()


# search 样例
# from elasticsearch_dsl.query import Match, MatchPhrasePrefix, Regexp
# from elasticsearch_dsl import Date, Text, Float
# from elasticsearch_dsl import Q
# import re
# def stock_search(word):
#     must, must_not, should, filters = [], [], [], []
#     ss = FundSearchDoc.search()
#     zh_model = re.compile(u'[a-z]')
#     if word.isdigit():
#         should.append(Regexp(order_book_id='.*{}'.format(word)))
#         should.append(Regexp(order_book_id='.*{}.*'.format(word)))
#         should.append(MatchPhrasePrefix(order_book_id=word))
#     elif zh_model.search(word):
#         should.append(MatchPhrasePrefix(desc_name_list=word))
#     else:
#         should.append(Match(desc_name=word))
#         should.append(Match(desc_name_index=word))
#
#     offset = 0
#     limit = 20
#     should_match = 1  # if should else 0
#     s = ss.query(Q(
#         'bool',
#         must=must,
#         filter=filters,
#         must_not=must_not,
#         should=should,
#         minimum_should_match=should_match
#     ))
#
#     _ = s[offset: offset + limit].execute()
#     print(_)
#     count = _.hits.total
#     return _.hits, count
#
# r, c = stock_search('富国')
# print(c)
# for i in r:
#     print(i.to_dict())


from robo.utils.es.es_models import StrategySearchDoc
from robo.utils.es.es_searcher import StrategySearcher









