from bases.dbwrapper import BaseModel, db


class WeChatPublicAccount(BaseModel):
    """微信公众号"""
    __tablename__ = "wechat_public_account"

    id = db.Column(db.Integer, primary_key=True)                    # 编号
    wxname = db.Column(db.CHAR(128))                                # 公众号名称
    wxid = db.Column(db.CHAR(128))                                  # 公众号微信 ID
    account_owner = db.Column(db.Text, default='')                  # 公众号主体
    account_type = db.Column(db.CHAR(128))                          # 公众号类型
    description = db.Column(db.Text)                                # 公众号介绍
    importance = db.Column(db.Integer)                              # 重要性
    crawled = db.Column(db.Integer)                                 # 是否抓取

    @classmethod
    def get_public_accounts(cls):
        accounts = cls.query.filter(
            cls.is_deleted == False,
        ).all()
        return [
            {
                'wxid': account.wxid,
                'wxname': account.wxname,
            } for account in accounts
        ]

    @classmethod
    def get_public_account_detail(cls, wxid):
        account = db.session.query(cls).filter_by(wxid=wxid).one_or_none()
        return {
            'wxid': account.wxid,
            'wxname': account.wxname,
            'account_owner': account.account_owner,
            'account_type': account.account_type,
            'description': account.description,
        } if account else {}

class WeChatArticle(BaseModel):
    """微信文章"""
    __tablename__ = "wechat_article"

    id = db.Column(db.Integer, primary_key=True)                    # 编号
    wxid = db.Column(db.CHAR(128))                                  # 文章所属公众号微信 ID
    wxname = db.Column(db.CHAR(128))                                # 文章所属公众号名称
    doc_id = db.Column(db.CHAR(16))                                 # 文章 ID
    seq = db.Column(db.Integer)                                     # 批次
    url = db.Column(db.Text)                                        # 文章 URL
    title = db.Column(db.Text)                                      # 文章标题
    cover = db.Column(db.Text)                                      # 文章封面图 URL
    doc_ct = db.Column(db.DATETIME)                                 # 文章创建时间
    read = db.Column(db.Integer)                                    # 阅读数
    like = db.Column(db.Integer)                                    # 点赞数
    click_ts = db.Column(db.Integer)                                # 文章点击时间戳

    @classmethod
    def get_article_count(cls, wxids=[], start_time=None, end_time=None):
        query = cls.query.filter(
            cls.is_deleted == False,
        )
        if wxids:
            query = query.filter(
                cls.wxid.in_(wxids)
            )
        if start_time:
            query = query.filter(
                cls.doc_ct >= start_time
            )
        if end_time:
            query = query.filter(
                cls.doc_ct <= end_time
            )
            
        article_count = query.count()
        return {
            'count': article_count
        }
        
    @classmethod
    def get_articles(cls, wxids=[], page_index=0, page_size=20, start_time=None, end_time=None):
        query = cls.query.filter(
            cls.is_deleted == False,
        )
        if wxids:
            query = query.filter(
                cls.wxid.in_(wxids)
            )
        if start_time:
            query = query.filter(
                cls.doc_ct >= start_time
            )
        if end_time:
            query = query.filter(
                cls.doc_ct <= end_time
            )
        if page_index < 0 or page_size <= 0 and page_size > 100:
            page_index = 0
            page_size = 20

        articles = query.limit(page_size).offset(page_index).all()
        return [
            {
                'id': article.id,
                'wxid': article.wxid,
                'wxname': article.wxname,
                'url': article.url,
                'title': article.title,
                'cover': article.cover,
                'doc_ct': article.doc_ct
            } for article in articles
        ]
