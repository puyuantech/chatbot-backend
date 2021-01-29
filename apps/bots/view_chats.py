
import datetime
import json

from flask import current_app

from bases.viewhandler import ApiViewHandler
from extensions.rsvp import RsvpBot, RsvpResponse
from extensions.wxwork import WxWorkNotification
from extensions.zidou import ZiDouBot
from models import ChatbotUserInfo, WechatGroupBotConfig
from utils.decorators import login_required, params_required

from .libs.chats import get_wechat_group_bot_config
from .libs.dialogs import save_chatbot_dialog


class GroupListAPI(ApiViewHandler):

    @login_required
    def get(self):
        """查询微信群列表(TODO: 分页)"""
        return ZiDouBot.get_wechat_group_list(
            current_app.chatroom_member_info_dict,
            current_app.chatroom_zidou_account_dict
        )


class GroupBotConfigAPI(ApiViewHandler):

    @login_required
    @params_required(*['wechat_group_id'])
    def get(self):
        """查询微信群对话机器人配置"""
        return get_wechat_group_bot_config(self.input.wechat_group_id)

    @login_required
    @params_required(*['wechat_group_id', 'bot_id', 'share_token'])
    def post(self):
        """设置微信群对话机器人配置"""
        WechatGroupBotConfig.update_bot_config(
            self.input.wechat_group_id, self.input.bot_id,
            self.input.share_token, self.input.stage, self.input.be_at
        )
        return 'success'


class ChatBotInfoAPI(ApiViewHandler):

    def get(self):
        """获取聊天机器人信息（用于小程序前端展示）"""
        rsvp_bot = RsvpBot.get_rsvp_bot()
        return rsvp_bot.get_bot_info()


class ChatFromMiniAPI(ApiViewHandler):

    @params_required(*['query', 'user_id'])
    def post(self):
        """聊天"""
        rsvp_bot = RsvpBot.get_rsvp_bot()
        resp = rsvp_bot.get_bot_response(self.input.query, f'openidprism_{self.input.user_id}')
        if not resp:
            return resp

        similarity, bot_reply, _ = RsvpResponse(resp.get('stage', [])).parse_stages()
        bot_raw_reply = json.dumps(resp, ensure_ascii=False)
        save_chatbot_dialog(self.input.user_id, self.input.query, bot_reply, bot_raw_reply, similarity, datetime.datetime.now())

        return resp


class ChatFromWechatAPI(ApiViewHandler):

    @params_required(*['query', 'user_id'])
    def post(self):
        """微信群成员聊天记录及回复"""
        chatroom_member_info_dict = current_app.chatroom_member_info_dict

        msg_id = self.input.msg_id
        username = self.input.username
        chatroomname = self.input.chatroomname
        content = self.input.content

        # 如果是机器人发言
        if username == self.input.bot_username:
            return

        if self.input.type != 'text' or not content:
            return

        zidou_bot = ZiDouBot.get_chatroom_zidou_bot(chatroomname, current_app.chatroom_zidou_account_dict)

        if username not in chatroom_member_info_dict.get(chatroomname, {}):
            chatroom_member_info_dict[chatroomname] = zidou_bot.get_member_info(chatroomname)
            if username not in chatroom_member_info_dict[chatroomname]:
                current_app.logger.warning(f'Failed processing msg {msg_id}: user {username} not found in {chatroomname}')
                return

        wechat_group_bot_config = get_wechat_group_bot_config(chatroomname)
        if wechat_group_bot_config['be_at']:
            bot_nickname = zidou_bot.nickname
            bot_be_at = f'@{bot_nickname}' in content
            if not bot_be_at:
                current_app.logger.info(f'Quit procssing msg {msg_id}: bot has not been @')
                return

            content = content.replace(f'@{bot_nickname}\u2005', '')
            content = content.replace(f'@{bot_nickname} ', '')
            if content.endswith(f'@{bot_nickname}'):
                content = content[:-len(f'@{bot_nickname}')]

        current_app.logger.info(f'Start requesting RSVP for msg {msg_id}, content: {content}')
        rsvp_group = RsvpBot.get_rsvp_bot(wechat_group_bot_config['bot_id'], wechat_group_bot_config['share_token'])

        ts = datetime.datetime.now()
        nick_name = chatroom_member_info_dict[chatroomname][username]['nickname']
        avatar_url = chatroom_member_info_dict[chatroomname][username]['avatar_url']
        user_id = ChatbotUserInfo.user_active_by_wechat(username, ts, nick_name, avatar_url)
        if not user_id:
            current_app.logger.warning(f'Failed processing msg {msg_id}: cannot get user_id for user {username}')
            return

        uid = f'openidgroup_{username}'
        try:
            resp = rsvp_group.get_bot_response(content, uid, wechat_group_bot_config['stage'])
        except Exception as e:
            import traceback
            current_app.logger.error(traceback.format_exc())
            resp = None

        if not resp:
            current_app.logger.warning(f'Failed to get rsvp response for msg {msg_id}, content: {content}')
            return
        current_app.logger.info(f'resp: {resp}')
        if resp.get('topic', 'fallback') != 'fallback' or wechat_group_bot_config['be_at']:
            similarity, bot_reply, start_miniprogram = RsvpResponse(
                resp.get('stage', []),
                chatroomname,
                wechat_group_bot_config['be_at']
            ).parse_stages()

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
            bot_reply, similarity = '', 0
            bad_case = f'Bad case:\n{nick_name}: {content}'
            WxWorkNotification(current_app.logger).send(bad_case)

        bot_raw_reply = json.dumps(resp, ensure_ascii=False)
        save_chatbot_dialog(user_id, content, bot_reply, bot_raw_reply, similarity, ts, chatroomname)
        return 'success'

