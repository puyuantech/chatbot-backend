
from datetime import datetime
from bases.globals import db
from models import WeChatGroupMessage, User

def save_text_message(user_id, chatroomname, text, ts=datetime.now()):
    WeChatGroupMessage(
        user_id=user_id,
        chatroomname=chatroomname,
        message_type='text',
        text=text,
        ts=ts,
    ).save()

def save_link_message(user_id, chatroomname, link_source_url, link_title, link_description, link_image_url,
                      ts=datetime.now()):
    WeChatGroupMessage(
        user_id=user_id,
        chatroomname=chatroomname,
        link_source_url=link_source_url,
        message_type='link',
        link_title=link_title,
        link_description=link_description,
        link_image_url=link_image_url,
        ts=ts
    ).save()

def save_pic_message(user_id, chatroomname, pic_url, ts=datetime.now()):
    WeChatGroupMessage(
        user_id=user_id,
        chatroomname=chatroomname,
        message_type='pic',
        pic_url=pic_url,
        ts=ts,
    ).save()

def get_message_count(chatroomnames=[], start_time=None, end_time=None):
    return WeChatGroupMessage.get_message_count(chatroomnames, start_time, end_time)

def get_messages(chatroomnames=[], page_index=0, page_size=20, start_time=None, end_time=None):
    messages = WeChatGroupMessage.get_messages(chatroomnames, page_index, page_size, start_time, end_time)
    user_ids = []
    for message in messages:
        user_ids.append(message['user_id'])
    query = User.filter_by_query().filter(User.id.in_(user_ids))
    users = query.all()
    user_name_dict = {}
    for user in users:
        user_dict = user.to_normal_dict()
        user_name_dict[user_dict['id']] = user_dict['nick_name']
    for message in messages:
        message['user_name'] = user_name_dict.get(message['user_id'], '')

    # TODO: chatroom nick name
    result = {
        'total': get_message_count(chatroomnames, start_time, end_time),
        'data': messages
    }
    return result
