import pandas as pd
from datetime import datetime

from pandas._libs.tslibs import Timestamp
from bases.globals import db
from models import WeChatArticle
from apps import create_app

def get_account_mapping():
    filename = '/shared/chat-bot/temp/public_accounts.xlsx'
    df = pd.read_excel(filename)
    df = df[['是否抓取', '重要性', '名称', '微信号', '主体', '类型', '介绍']]
    df.columns = ['crawled', 'importance', 'wxname', 'wxid', 'account_owner', 'account_type', 'description']
    df = df.dropna()

    return {
        row.wxid: row.wxname for row in df.itertuples(index=False)
    }

if __name__ == "__main__":
    account_mapping = get_account_mapping()
    # print(account_mapping)

    # filename = '/shared/chat-bot/log/part_articles.xlsx'
    filename = '/shared/chat-bot/log/history.xlsx'
    df = pd.read_excel(filename)
    df = df.drop(['id'], axis=1)
    df.columns = ['wxid', 'doc_id', 'seq', 'url', 'title', 'cover', 'doc_ct', 'read', 'like', 'click_ts']
    df = df.dropna(subset=['wxid'])

    df['doc_ct'] = df['doc_ct'].map(lambda x: pd.to_datetime(x, unit='s'))
    df['wxname'] = df['wxid'].map(lambda x: account_mapping.get(x))
    df['create_time'] = datetime.now()
    df['update_time'] = datetime.now()
    # print(df)
    # exit()

    app = create_app()
    with app.app_context():
        df.to_sql(WeChatArticle.__table__.name, db.engine, index=False, if_exists='append')
