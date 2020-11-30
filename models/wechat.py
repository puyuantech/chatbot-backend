from bases.dbwrapper import BaseModel, db


class WeChatUnionID(BaseModel):
    """用户微信绑定"""
    __tablename__ = "user_wx"

    id = db.Column(db.Integer, primary_key=True)                    # 编号
    union_id = db.Column(db.CHAR(128))                              # 开放平台union_id
    open_id = db.Column(db.CHAR(128), default='')                   # 公众号(服务号)
    user_id = db.Column(db.Integer, db.ForeignKey('chatbot_user_info.id'))
    user = db.relationship('ChatbotUserInfo', backref='union_id')

    @classmethod
    def get_user_id(cls, union_id):
        user_wx = cls.filter_by_query(
            union_id=union_id
        ).first()
        if not user_wx:
            return None
        return user_wx.user_id
