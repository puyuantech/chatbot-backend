from elasticsearch_dsl import Document, Date, Text, Keyword


class WeChatOASearchDoc(Document):

    oa_id = Keyword()
    wx_name = Text(analyzer='ik_max_word')
    wx_name_pinyin = Text(analyzer='pinyin')
    wx_name_first = Text(analyzer='standard')
    update_time = Date()
    create_time = Date()

    class Index:
        name = 'wx_pa'
        label_name = 'es_test'


class WeChatOAArticleSearchDoc(Document):

    article_id = Keyword()
    article_title = Text(analyzer='ik_max_word')
    article_title_pinyin = Text(analyzer='pinyin')
    article_title_first = Text(analyzer='standard')
    update_time = Date()
    create_time = Date()

    class Index:
        name = 'wx_article'
        label_name = 'es_test'

