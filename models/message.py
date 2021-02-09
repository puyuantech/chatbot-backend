from bases.dbwrapper import BaseModel, db


class WeChatGroupMessage(BaseModel):
    """微信群发消息记录"""
    __tablename__ = "wechat_group_message"

    id = db.Column(db.Integer, primary_key=True)                    # 编号
    user_id = db.Column(db.Integer)                                 # 用户ID
    chatroomname = db.Column(db.Text)                               # 微信群名称
    message_type = db.Column(db.Text)                               # 消息类型: text, link, pic
    text = db.Column(db.Text)                                       # 文本消息内容
    link_source_url = db.Column(db.Text)                            # 链接消息url
    link_title = db.Column(db.Text)                                 # 链接消息标题
    link_description = db.Column(db.Text)                           # 链接消息描述
    link_image_url = db.Column(db.Text)                             # 链接消息图片
    pic_url = db.Column(db.Text)                                    # 图片消息url
    ts = db.Column(db.DATETIME)                                     # 消息时间戳


    @classmethod
    def get_message_count(cls, chatroomnames=[], start_time=None, end_time=None):
        query = cls.query.filter(
            cls.is_deleted == False,
        )
        if chatroomnames:
            query = query.filter(
                cls.chatroomname.in_(chatroomnames)
            )
        if start_time:
            query = query.filter(
                cls.ts >= start_time
            )
        if end_time:
            query = query.filter(
                cls.ts <= end_time
            )
            
        message_count = query.count()
        return {
            'count': message_count
        }
        
    @classmethod
    def get_messages(cls, chatroomnames=[], page_index=0, page_size=20, start_time=None, end_time=None):
        query = cls.query.filter(
            cls.is_deleted == False,
        )
        if chatroomnames:
            query = query.filter(
                cls.chatroomname.in_(chatroomnames)
            )
        if start_time:
            query = query.filter(
                cls.ts >= start_time
            )
        if end_time:
            query = query.filter(
                cls.ts <= end_time
            )
        if page_index < 0 or page_size <= 0 and page_size > 100:
            page_index = 0
            page_size = 20

        messages = query.limit(page_size).offset(page_index*page_size).all()
        return [
            {
                'id': message.id,
                'user_id': message.user_id,
                'chatroomname': message.chatroomname,
                'message_type': message.message_type,
                'text': message.text,
                'link_source_url': message.link_source_url,
                'link_title': message.link_title,
                'link_description': message.link_description,
                'link_image_url': message.link_image_url,
                'pic_url': message.pic_url,
                'ts': message.ts
            } for message in messages
        ]
