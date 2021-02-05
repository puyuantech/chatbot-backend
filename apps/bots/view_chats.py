
import datetime
import json
import traceback

from flask import current_app

from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from extensions.rsvp import RsvpBot, RsvpResponse
from extensions.zidou import ZiDouBot
from models import ChatbotUserInfo, WechatGroupBotConfig
from utils.decorators import login_required, params_required

from .libs.chats import get_nick_name_and_avatar_url, get_wechat_group_bot_config, parse_bot_response, replace_content
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
        current_app.logger.info(f'[ChatFromMiniAPI] (input){self.input}')

        try:
            rsvp_bot = RsvpBot.get_rsvp_bot()
            resp = rsvp_bot.get_bot_response(self.input.query, f'openidprism_{self.input.user_id}')
            current_app.logger.info(f'[ChatFromMiniAPI] rsvp (response){resp}')
        except Exception:
            current_app.logger.error(f'[ChatFromMiniAPI] rsvp (Exception){traceback.format_exc()}')
            resp = None

        if not resp:
            raise LogicError(f'[ChatFromMiniAPI] Failed to get rsvp response for content: {self.input.query}')

        similarity, bot_reply, _ = RsvpResponse(resp.get('stage', [])).parse_stages()
        bot_raw_reply = json.dumps(resp, ensure_ascii=False)
        save_chatbot_dialog(self.input.user_id, self.input.query, bot_reply, bot_raw_reply, similarity, datetime.datetime.now())

        return resp


class ChatFromWechatAPI(ApiViewHandler):

    @params_required(*['content'])
    def post(self):
        """微信群成员聊天记录及回复"""
        current_app.logger.info(f'[ChatFromWechatAPI] (input){self.input}')

        msg_id, username, chatroomname, content = self.input.msg_id, self.input.username, self.input.chatroomname, self.input.content

        # 如果是机器人发言
        if username == self.input.bot_username:
            return

        if self.input.type != 'text':
            return

        zidou_bot = ZiDouBot.get_chatroom_zidou_bot(chatroomname, current_app.chatroom_zidou_account_dict)
        nick_name, avatar_url = get_nick_name_and_avatar_url(username, chatroomname, msg_id, zidou_bot)

        bot_config = get_wechat_group_bot_config(chatroomname)
        be_at, bot_id, share_token, stage = bot_config['be_at'], bot_config['bot_id'], bot_config['share_token'], bot_config['stage']

        if be_at:
            if f'@{zidou_bot.nickname}' not in content:
                current_app.logger.info(f'[ChatFromWechatAPI] Quit procssing msg {msg_id}: bot has not been @')
                return

            content = replace_content(content, zidou_bot.nickname)

        current_app.logger.info(f'[ChatFromWechatAPI] Start requesting RSVP for msg {msg_id}, content: {content}')

        ts = datetime.datetime.now()
        user_id = ChatbotUserInfo.user_active_by_wechat(username, ts, nick_name, avatar_url)
        if not user_id:
            raise LogicError(f'[ChatFromWechatAPI] Failed processing msg {msg_id}: cannot get user_id for user {username}')

        try:
            rsvp_bot = RsvpBot.get_rsvp_bot(bot_id, share_token)
            resp = rsvp_bot.get_bot_response(content, f'openidgroup_{username}', stage)
            current_app.logger.info(f'[ChatFromWechatAPI] rsvp (response){resp}')
        except Exception:
            current_app.logger.error(f'[ChatFromWechatAPI] rsvp (Exception){traceback.format_exc()}')
            resp = None

        if not resp:
            raise LogicError(f'[ChatFromWechatAPI] Failed to get rsvp response for msg {msg_id}, content: {content}')

        similarity, bot_reply = parse_bot_response(resp, be_at, chatroomname, content, username, msg_id, nick_name, zidou_bot)
        bot_raw_reply = json.dumps(resp, ensure_ascii=False)
        save_chatbot_dialog(user_id, content, bot_reply, bot_raw_reply, similarity, ts, chatroomname)
        return 'success'

