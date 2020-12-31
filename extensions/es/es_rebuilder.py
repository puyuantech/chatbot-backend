import pandas as pd
from apps import create_app
from extensions.es.es_builder import WeChatOABuilder, WeChatOAArticleBuilder
from extensions.es.es_models import WeChatOASearchDoc, WeChatOAArticleSearchDoc
from models import WeChatArticle, WeChatPublicAccount, db


def we_chat_oa_rebuilder():
    builder = WeChatOABuilder(label='es_test', doc_model=WeChatOASearchDoc)
    builder.init_rebuild_index()

    query = db.session.query(WeChatPublicAccount)
    df = pd.read_sql(query.statement, query.session.bind)
    print(df)
    for index in df.index:
        param = builder.build_doc_param(
            df.loc[index, 'id'],
            df.loc[index, 'wxname'],
        )
        builder.add_bulk_data(df.loc[index, 'id'], param)
    builder.done_rebuild_index()


def we_chat_article_rebuilder():
    builder = WeChatOAArticleBuilder(label='es_test', doc_model=WeChatOAArticleSearchDoc)
    builder.init_rebuild_index()

    query = db.session.query(WeChatArticle)
    df = pd.read_sql(query.statement, query.session.bind)
    print(df)
    for index in df.index:
        param = builder.build_doc_param(
            df.loc[index, 'id'],
            df.loc[index, 'title'],
        )
        builder.add_bulk_data(df.loc[index, 'id'], param)
    builder.done_rebuild_index()


def re_build():
    with create_app().app_context():
        we_chat_oa_rebuilder()
        print('WeChat public account rebuilder done!')

        we_chat_article_rebuilder()
        print('WeChat article rebuilder done!')


if __name__ == '__main__':
    re_build()
