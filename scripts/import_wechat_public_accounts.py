import pandas as pd
from datetime import datetime
from bases.globals import db
from models import WeChatPublicAccount
from apps import create_app

if __name__ == "__main__":
    filename = '/shared/chat-bot/temp/public_accounts.xlsx'
    df = pd.read_excel(filename)
    df = df[['是否抓取', '重要性', '名称', '微信号', '主体', '类型', '介绍']]
    df.columns = ['crawled', 'importance', 'wxname', 'wxid', 'account_owner', 'account_type', 'description']
    df = df.dropna()
    df['create_time'] = datetime.now()
    df['update_time'] = datetime.now()
    # print(df)
    # exit()

    app = create_app()
    with app.app_context():
        df.to_sql(WeChatPublicAccount.__table__.name, db.engine, index=False, if_exists='append')
