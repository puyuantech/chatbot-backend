from elasticsearch_dsl import Document, Date, Text, Keyword, Integer


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
    wxname = Keyword()
    doc_ct = Date()
    doc_id = Text()
    url = Text()
    title = Text()
    cover = Text()
    read = Integer()
    like = Integer()
    click_ts = Integer()
    update_time = Date()
    create_time = Date()

    class Index:
        name = 'wx_article'
        label_name = 'es_test'

    def to_dict(self, include_meta=False, skip_empty=True):
        return {
            'id': self.article_id,
            'wxname': self.wxname,
            'doc_id': self.doc_id,
            'url': self.url,
            'title': self.title,
            'cover': self.cover,
            'read': self.read,
            'like': self.like,
            'doc_ct': self.doc_ct,
            'click_ts': self.click_ts,
            'update_time': self.update_time,
            'create_time': self.create_time,
        }

