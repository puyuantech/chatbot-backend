import uuid
import  datetime
from bases.dbwrapper import db, BaseModel
from bases.constants import TOKEN_MAX_NUM, TOKEN_EXPIRATION_IN_MINUTES


class ChatbotUserInfo(BaseModel):
    '''对话机器人用户信息'''
    __tablename__ = 'chatbot_user_info'

    id = db.Column(db.Integer, primary_key=True)                # 数据行编号
    wechat_user_name = db.Column(db.CHAR(32), default='')       # 用户微信号
    nick_name = db.Column(db.CHAR(32), default='')              # 昵称
    head_img = db.Column(db.Text, default='')                   # 头像
    expertise = db.Column(db.FLOAT, default=0)                  # 用户专业度，-1或者[0, 1.0]间，-1表示未初始化，其余值越大代表越专业
    risk_tolerance = db.Column(db.FLOAT, default=0)             # 用户风险承受能力，-1或者[0, 1.0]间，-1表示未初始化，其余值越大代表风险承受能力越强
    last_action_ts = db.Column(db.DATETIME)                     # 最新活动时间戳

    def readable_expertise(self):
        if self.expertise < 0.15:
            return '低'
        elif self.expertise < 0.35:
            return '较低'
        elif self.expertise < 0.65:
            return '中等'
        elif self.expertise < 0.85:
            return '较高'
        else:
            return '高'

    def readable_risk_tolerance(self):
        if self.risk_tolerance <= 0.38:
            return '安逸型'
        elif self.risk_tolerance <= 0.52:
            return '保守型'
        elif self.risk_tolerance <= 0.68:
            return '稳健型'
        elif self.risk_tolerance <= 0.84:
            return '积极型'
        else:
            return '进取型'

    def to_dict(self, fields_list=None, remove_fields_list=None, remove_deleted=True):
        data = super().to_dict(fields_list, remove_fields_list, remove_deleted)
        data['expertise'] = self.readable_expertise()
        data['risk_tolerance'] = self.readable_risk_tolerance()
        return data


class ChatBotToken(BaseModel):
    """
    用户token
    """
    __tablename__ = "chatbot_tokens"

    id = db.Column(db.Integer, primary_key=True)                # 编号
    key = db.Column(db.String(32))                              # key值
    refresh_key = db.Column(db.String(32))                      # 刷新key值
    expires_at = db.Column(db.DateTime, nullable=False)         # 过期时间
    user_id = db.Column(db.Integer, db.ForeignKey('chatbot_user_info.id'))
    user = db.relationship('ChatbotUserInfo', backref='token')

    @staticmethod
    def generate_key():
        return uuid.uuid4().hex

    @staticmethod
    def generate_expires_at():
        return datetime.datetime.now() + datetime.timedelta(minutes=TOKEN_EXPIRATION_IN_MINUTES)

    def is_valid(self):
        return datetime.datetime.now() < self.expires_at

    def refresh(self, refresh_key):
        if self.refresh_key == refresh_key:
            self.key = self.generate_key()
            self.expires_at = self.generate_expires_at()

    @classmethod
    def generate_token(cls, user_id):
        tokens = cls.filter_by_query(
            user_id=user_id,
        ).order_by(cls.expires_at.asc()).all()

        if len(tokens) < TOKEN_MAX_NUM:
            token = cls.create(
                key=cls.generate_key(),
                refresh_key=cls.generate_key(),
                expires_at=cls.generate_expires_at(),
                user_id=user_id,
            )
        else:
            token = tokens[0]
            token.refresh(token.refresh_key)
            token.save()

        token = cls.get_by_id(token.id)
        return token.to_dict()


class ChatbotDialogStat(BaseModel):
    '''对话机器人对话量日度统计'''
    __tablename__ = 'chatbot_dialog_stat'

    id = db.Column(db.Integer, primary_key=True)                # 数据行编号
    user_id = db.Column(db.Integer)                             # 用户ID
    dialog_count = db.Column(db.Integer)                        # 用户对话数
    ts = db.Column(db.DATETIME)                                 # 时间戳
    wechat_group_id = db.Column(db.CHAR(32))                    # 微信群ID（如有）


class ChatbotUserStat(BaseModel):
    '''对话机器人用户数日度统计'''
    __tablename__ = 'chatbot_user_stat'

    id = db.Column(db.Integer, primary_key=True)                # 数据行编号
    user_count = db.Column(db.Integer)                          # 总用户数
    active_user_count = db.Column(db.Integer)                   # 活跃用户数
    ts = db.Column(db.DATETIME)                                 # 时间戳


class ChatbotDialog(BaseModel):
    '''对话机器人用户对话'''
    __tablename__ = 'chatbot_dialog'

    id = db.Column(db.Integer, primary_key=True)                # 数据行编号
    user_id = db.Column(db.Integer)                             # 用户ID
    user_input = db.Column(db.Text)                             # 用户输入
    bot_reply = db.Column(db.Text)                              # 机器人回答
    bot_raw_reply = db.Column(db.Text)                          # 机器人原始回答
    similarity = db.Column(db.FLOAT(asdecimal=False))           # 用户输入与模型匹配分数
    session_id = db.Column(db.CHAR(32))                         # 会话ID
    ts = db.Column(db.DATETIME)                                 # 对话时间戳
    wechat_group_id = db.Column(db.CHAR(32))                    # 微信群ID（如有）


class ChatbotProductView(BaseModel):
    '''对话机器人产品访问'''
    __tablename__ = 'chatbot_product_view'

    id = db.Column(db.Integer, primary_key=True)                # 数据行编号
    user_id = db.Column(db.Integer)                             # 用户ID
    wechat_group_id = db.Column(db.CHAR(32))                    # 微信群ID（如有）
    product_id = db.Column(db.CHAR(32))                         # 产品ID
    product_type = db.Column(db.CHAR(32))                       # 产品类型
    product_name = db.Column(db.CHAR(64))                       # 产品名称
    ts = db.Column(db.DATETIME)                                 # 产品访问时间戳


class ChatbotProductDailyView(BaseModel):
    '''对话机器人产品访问量日度统计'''
    __tablename__ = 'chatbot_product_daily_view'

    id = db.Column(db.Integer, primary_key=True)                # 数据行编号
    user_id = db.Column(db.Integer)                             # 用户ID
    wechat_group_id = db.Column(db.CHAR(32))                    # 微信群ID（如有）
    product_view_count = db.Column(db.Integer)                  # 用户产品访问量
    ts = db.Column(db.DATETIME)                                 # 时间戳


# class ChatbotProductStat(BaseDataModel, DBMixin):
#     '''对话机器人产品访问统计'''
#     __tablename__ = 'chatbot_product_stat'

#     id = db.Column(db.Integer, primary_key=True)              # 数据行编号
#     product_id = db.Column(db.CHAR(32))                       # 产品ID
#     product_type = db.Column(db.CHAR(32))                     # 产品类型
#     view_count = db.Column(db.Integer, default=0)             # 产品访问次数
#     ts = db.Column(DATETIME)                                  # 产品访问时间戳


class ChatbotTag(BaseModel):
    '''对话机器人标签列表'''
    __tablename__ = 'chatbot_tags'

    tag_name = db.Column(db.String(16), primary_key=True)  # 标签名称
    user_id = db.Column(db.Integer)                        # 用户ID


class ChatbotDialogTag(BaseModel):
    '''对话机器人对话标签'''
    __tablename__ = 'chatbot_dialog_tags'

    id = db.Column(db.Integer, primary_key=True)  # 数据行编号
    tag_name = db.Column(db.String(16))           # 标签名称
    dialog_id = db.Column(db.Integer)             # 对话ID
    add_user_id = db.Column(db.Integer)           # 添加者ID
    del_user_id = db.Column(db.Integer)           # 删除者ID


class WechatGroupBotConfig(BaseModel):
    '''微信群对话机器人配置'''
    __tablename__ = 'wechat_group_bot_config'

    id = db.Column(db.Integer, primary_key=True)                # 数据行编号
    wechat_group_id = db.Column(db.CHAR(32))                    # 微信群ID
    bot_id = db.Column(db.Integer)                              # Bot ID
    share_token = db.Column(db.Text)                            # Bot share token
    stage = db.Column(db.Text)                                  # Bot stage (release/test)
    be_at = db.Column(db.Integer)                               # 是否需要at才回复
