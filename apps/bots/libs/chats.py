
from flask import current_app

from bases.exceptions import LogicError
from bases.globals import db, settings
from extensions.rsvp import RsvpJson
from extensions.wxwork import WxWorkNotification
from extensions.zidou import ZiDou
from models import WechatGroupBotConfig


def get_nick_name_and_avatar_url(username, chatroomname, msg_id, zidou_bot: ZiDou):
    chatroom_member_info_dict = current_app.chatroom_member_info_dict

    if username not in chatroom_member_info_dict.get(chatroomname, {}):
        chatroom_member_info_dict[chatroomname] = zidou_bot.get_member_info(chatroomname)
        if username not in chatroom_member_info_dict[chatroomname]:
            raise LogicError(f'Failed processing msg {msg_id}: user {username} not found in {chatroomname}')

    user_info = chatroom_member_info_dict[chatroomname][username]
    return user_info['nickname'], user_info['avatar_url']


def get_wechat_group_bot_config(wechat_group_id):
    bot_config = db.session.query(WechatGroupBotConfig).filter_by(wechat_group_id=wechat_group_id).one_or_none()

    result = {'wechat_group_id': wechat_group_id}
    if not bot_config:
        rsvp_group_conf = settings['THIRD_SETTING']['rsvp_group']
        result['bot_id'] = rsvp_group_conf['bot_id']
        result['share_token'] = rsvp_group_conf['share_token']
        result['stage'] = 'release'
        result['be_at'] = 0
    else:
        result['bot_id'] = bot_config.bot_id
        result['share_token'] = bot_config.share_token
        result['stage'] = bot_config.stage
        result['be_at'] = bot_config.be_at

    return result


def parse_bot_response(response, be_at, chatroomname, content, username, msg_id, nick_name, zidou_bot: ZiDou):
    similarity, bot_reply = 0, ''

    if response.get('topic', 'fallback') != 'fallback' or be_at:
        similarity, bot_reply, start_miniprogram, _ = RsvpJson(response, chatroomname, be_at).parse_response()

        if bot_reply:
            zidou_bot.at_somebody(chatroomname, username, '', f'\n{bot_reply}')
        else:
            current_app.logger.warning(f'Failed to get bot reply for {msg_id}, content: {content}')

        if start_miniprogram:
            miniprogram_id_and_ts = zidou_bot.get_miniprogram_id_and_ts('棱小镜')
            if miniprogram_id_and_ts and not bot_reply:
                zidou_bot.at_somebody(chatroomname, username, '', f'\n请打开下面小程序：')
                zidou_bot.send_miniprogram_message(chatroomname, miniprogram_id_and_ts[0])

    else:
        bad_case = f'Bad case:\n{nick_name}: {content}'
        WxWorkNotification(current_app.logger).send(bad_case)

    return similarity, bot_reply


def replace_content(content, bot_nickname):
    content = content.replace(f'@{bot_nickname}\u2005', '')
    content = content.replace(f'@{bot_nickname} ', '')
    if content.endswith(f'@{bot_nickname}'):
        content = content[:-len(f'@{bot_nickname}')]

    return content

