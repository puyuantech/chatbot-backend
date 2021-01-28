
from flask import current_app

from bases.globals import settings

from .zidou import ZiDou


class ZiDouBot:

    zidou_conf: dict = settings['THIRD_SETTING']['zidou']

    @classmethod
    def get_zidou_bot_dict(cls):
        return {
            phone: ZiDou(conf['url'], conf['secret'], phone, conf['bot_nickname'])
            for phone, conf in cls.zidou_conf.items()
        }

    @classmethod
    def get_chatroom_zidou_bot(cls, chatroomname, chatroom_zidou_account_dict):
        zidou_bot_dict = cls.get_zidou_bot_dict()

        if chatroomname not in chatroom_zidou_account_dict:
            for phone, zidou_bot in zidou_bot_dict.items():
                chatroom_list = zidou_bot.get_chatroom_list()
                for chatroom in chatroom_list:
                    chatroomname = chatroom.get('chatroomname')
                    chatroom_zidou_account_dict[chatroomname] = phone

        phone = chatroom_zidou_account_dict.get(chatroomname, '')
        if not phone:
            current_app.logger.error(f'Failed to send_msg, no related zidou bot for chatroomname: {chatroomname}')
            return None

        return zidou_bot_dict.get(phone, None)

    @classmethod
    def get_wechat_group_list(cls, chatroom_member_info_dict, chatroom_zidou_account_dict):
        # TODO: cache for 1 min
        zidou_bot_dict = cls.get_zidou_bot_dict()

        result = []
        for phone, zidou_bot in zidou_bot_dict.items():
            for chatroom in zidou_bot.get_chatroom_list():
                chatroomname, roomowner = chatroom.get('chatroomname'), chatroom.get('roomowner')
                owner_nick_name = owner_avatar_url = None

                chatroom_zidou_account_dict[chatroomname] = phone
                if roomowner not in chatroom_member_info_dict.get(chatroomname, {}):
                    chatroom_member_info_dict[chatroomname] = zidou_bot.get_member_info(chatroomname)

                chatroom_member_info = chatroom_member_info_dict.get(chatroomname, {})
                owner_nick_name = chatroom_member_info.get(roomowner, {}).get('nickname')
                owner_avatar_url = chatroom_member_info.get(roomowner, {}).get('avatar_url')

                result.append({
                    'nick_name': chatroom.get('nickname'),
                    'id': chatroomname,
                    'avatar_url': chatroom.get('avatar_url'),
                    'member_count': chatroom.get('member_count'),
                    'owner_nick_name': owner_nick_name,
                    'owner_avatar_url': owner_avatar_url
                })
        return result

