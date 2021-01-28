
import json

from datetime import datetime

from bases.globals import settings, db
from models import (ChatbotDialog, ChatbotDialogStat,
                    ChatbotUserInfo, WechatGroupBotConfig)
from extensions.cognai import Cognai
from extensions.rsvp import Rsvp
from extensions.url_manager import UrlManager
from extensions.wxwork import WxWorkNotification
from extensions.zidou import ZiDou

from .constants import Operation, TagType
from .libs.chats import get_user_dict, get_user_id_from_rsvp, save_chatbot_dialog, save_product_view
from .libs.tags import get_tags_by_dialog_id


class ChatbotLogic:

    def __init__(self, logger):
        self.conf = settings['THIRD_SETTING']
        self.logger = logger

    def get_cognai_dialog(self, q):
        '''
        获取 Cognai 回复
        '''
        cognai_conf = self.conf['cognai']
        cognai = Cognai(cognai_conf['url'], cognai_conf['user_account'], cognai_conf['user_pwd'])
        resp = cognai.get_response(q)
        output = ''
        stock_name = ''
        if resp and resp.get('code') == 0:
            answer = resp.get('answer', {})
            cognai_answer_columns = answer.get('columns', [])
            cognai_answer_data = answer.get('data', [])
            cognai_answer_series = answer.get('series', [])

            if cognai_answer_series:
                for series in cognai_answer_series:
                    if series.get('name') and series.get('data'):
                        output += f'{series.get("name")}：\n'
                        if not stock_name:
                            stock_name = series.get("name").split('-')[0]
                    for item in series.get('data', []):
                        output += f'{item[0]}: {round(item[1] * 100) / 100.0}\n'
            elif cognai_answer_data:
                for data in cognai_answer_data:
                    if data.get('index') and data.get('short_name'):
                        if not output:
                            output = '为您找到下列数据：\n'
                        if not stock_name:
                            stock_name = data.get("short_name")
                        output += f'{data.get("short_name")}({data.get("index")})\n'

        if not output:
            rsp = {
                "status": -1
            }
        else:
            rsp = {
                "stage": [
                    {
                        "text": {
                            "plainText": [
                                output
                            ],
                            "text": [
                                output
                            ],
                            "isRich": False
                        }
                    },
                    {
                        "quickReplies": {
                            "quickReplies": [
                                {
                                    "text": f"重仓{stock_name}的基金有哪些",
                                    "postback": f"重仓{stock_name}的基金有哪些？"
                                },
                                {
                                    "text": "我要投资",
                                    "postback": "我要投资。"
                                },
                                {
                                    "text": "推荐基金",
                                    "postback": "给我推荐基金。"
                                },
                                {
                                    "text": "搜索基金",
                                    "postback": "我想搜索基金。"
                                },
                                {
                                    "text": "特色榜单",
                                    "postback": "我想看看特色榜单。"
                                },
                                {
                                    "text": "个性化推荐",
                                    "postback": "为我进行个性化推荐。"
                                },
                                {
                                    "text": "我的画像",
                                    "postback": "查看我的画像。"
                                }
                            ]
                        }
                    }
                ],
                "status": 0
            }

        return rsp

    def get_user_list(self, top_n, wechat_group_id):
        user_dialog_count = ChatbotDialogStat.get_user_dialog_counts(top_n)

        query = ChatbotUserInfo.filter_by_query()
        if top_n:
            query = query.filter(ChatbotUserInfo.id.in_(user_dialog_count.keys()))
        users = query.all()

        result = [get_user_dict(user, user_dialog_count) for user in users]
        if top_n:
            result.sort(key=lambda item: item['dialog_count'], reverse=True)

        return result

    def get_user_info(self, user_id=None, rsvp_user_id=None):
        if not user_id:
            user_id = get_user_id_from_rsvp(rsvp_user_id, datetime.now())
        user = db.session.query(ChatbotUserInfo).filter_by(id=user_id).one_or_none()
        return get_user_dict(user) if user else {}

    def get_user_dialog(self, user_id, start=None, end=None):
        dialogs = ChatbotDialog.get_user_dialogs(user_id, start, end)
        result = []
        for dialog in dialogs:
            result.append({
                'tags': get_tags_by_dialog_id(dialog.id),
                **dialog.to_dict(remove_fields_list=['create_time', 'update_time']),
            })
        return result

    def get_wechat_group_dialog(self, wechat_group_id, start=None, end=None):
        # TODO: cache
        user_info_dict = {}
        users = ChatbotUserInfo.filter_by_query().all()
        for user in users:
            user_info_dict[user.id] = {
                'nick_name': user.nick_name,
                'head_img': user.head_img
            }

        dialogs = ChatbotDialog.get_group_dialogs(wechat_group_id, start, end)
        result = []
        for dialog in dialogs:
            dialog_dict = dialog.to_dict(remove_fields_list=['create_time', 'update_time'])
            dialog_dict['nickname'] = user_info_dict.get(dialog_dict['user_id'], {}).get('nick_name')
            dialog_dict['head_img'] = user_info_dict.get(dialog_dict['user_id'], {}).get('head_img')
            dialog_dict['tags'] = get_tags_by_dialog_id(dialog.id)

            result.append(dialog_dict)
        return result

    def get_wechat_group_bot_config(self, wechat_group_id):
        bot_config = db.session.query(WechatGroupBotConfig).filter_by(wechat_group_id=wechat_group_id).one_or_none()

        result = {
            'wechat_group_id': wechat_group_id
        }
        if not bot_config:
            rsvp_group_conf = self.conf['rsvp_group']
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

    def update_user_dialog(self, json_dict):
        if not json_dict:
            return
        req = json_dict.get('request')
        resp = json_dict.get('response')
        if not req or not resp:
            return

        ts = req.get('timestamp')
        if not ts:
            ts = datetime.now()
        else:
            ts = datetime.fromtimestamp(ts)

        user_id = get_user_id_from_rsvp(req.get('uid'), ts)
        if not user_id:
            return

        user_input = req.get('question')
        similarity, bot_reply, start_miniprogram = self._parse_rsvp_response_stages(resp.get('stage', []))

        bot_raw_reply = json.dumps(resp, ensure_ascii=False)

        save_chatbot_dialog(user_id, user_input, bot_reply, bot_raw_reply, similarity, ts)

    def update_user_tag(self, rsvp_user_id, tag_type, tag_value, operation):
        user_id = get_user_id_from_rsvp(rsvp_user_id, datetime.now())
        if not user_id:
            return

        chatbot_user = db.session.query(ChatbotUserInfo).filter_by(id=user_id).one_or_none()
        if not chatbot_user:
            return

        if tag_type == TagType.expertise:
            if operation == Operation.set:
                chatbot_user.expertise = float(tag_value)
            if operation == Operation.update:
                chatbot_user.expertise += float(tag_value)

            chatbot_user.expertise = min(chatbot_user.expertise, 1)
            chatbot_user.expertise = max(chatbot_user.expertise, 0)

        if tag_type == TagType.risk_tolerance:
            if operation == Operation.set:
                chatbot_user.risk_tolerance = float(tag_value)
            elif operation == Operation.update:
                chatbot_user.risk_tolerance += float(tag_value)

            chatbot_user.risk_tolerance = min(chatbot_user.risk_tolerance, 1)
            chatbot_user.risk_tolerance = max(chatbot_user.risk_tolerance, 0)

        db.session.commit()

    def update_user_product_view(self, rsvp_user_id, wechat_group_id, product_id, product_type, product_name, ts):
        # Valid rsvp_user_id is from Prism or Wechat Group, and skip user from other sources
        #   rsvp_user_id (from Prism) sample: openidprism_123
        #   rsvp_user_id (from Wechat Group) sample: openidgroup_xxx
        ts = ts if ts else datetime.now()
        if type(ts) is str:
            ts = datetime.fromisoformat(ts)

        user_id = get_user_id_from_rsvp(rsvp_user_id, ts)
        if not user_id:
            return

        save_product_view(user_id, product_id, product_type, product_name, ts, wechat_group_id)

    def get_rsvp_bot(self):
        rsvp_conf = self.conf['rsvp']
        return Rsvp(rsvp_conf['url'], rsvp_conf['bot_id'], rsvp_conf['share_token'], self.logger)

    def get_bot_info(self):
        rsvp_bot = self.get_rsvp_bot()
        resp = rsvp_bot.get_bot_info()
        return resp

    def mini_chat(self, query, user_id):
        ts = datetime.now()
        uid = f'openidprism_{user_id}'
        rsvp_bot = self.get_rsvp_bot()
        resp = rsvp_bot.get_bot_response(query, uid)
        if not resp:
            return

        similarity, bot_reply, _ = self._parse_rsvp_response_stages(resp.get('stage', []))
        bot_raw_reply = json.dumps(resp, ensure_ascii=False)
        save_chatbot_dialog(user_id, query, bot_reply, bot_raw_reply, similarity, ts)

        return resp

    def chat(self, json_dict):
        if not json_dict:
            return
        query = json_dict.get('query')
        user_id = json_dict.get('user_id')
        if not query or not user_id:
            return

        return self.mini_chat(query, user_id)

    def get_zidou_bot_dict(self):
        zidou_conf_dict = self.conf['zidou']
        zidou_bot_dict = {}
        for phone, zidou_conf in zidou_conf_dict.items():
            zidou_bot_dict[phone] = ZiDou(zidou_conf['url'], zidou_conf['secret'], phone, zidou_conf['bot_nickname'])
        return zidou_bot_dict

    def get_chatroom_zidou_bot(self, chatroomname, chatroom_zidou_account_dict):
        zidou_bot_dict = self.get_zidou_bot_dict()

        if chatroomname not in chatroom_zidou_account_dict:
            for phone, zidou_bot in zidou_bot_dict.items():
                chatroom_list = zidou_bot.get_chatroom_list()
                for chatroom in chatroom_list:
                    chatroomname = chatroom.get('chatroomname')
                    chatroom_zidou_account_dict[chatroomname] = phone

        phone = chatroom_zidou_account_dict.get(chatroomname, '')
        if not phone:
            self.logger.error(f'Failed to send_msg, no related zidou bot for chatroomname: {chatroomname}')
            return None

        return zidou_bot_dict.get(phone, None)


    def wechat_chatroom_msg_callback(self, json_dict, chatroom_member_info_dict, chatroom_zidou_account_dict):
        if not json_dict:
            return
        self.logger.info(json_dict)

        msg_id = json_dict.get('msg_id')
        username = json_dict.get('username')
        msg_type = json_dict.get('type')
        chatroomname = json_dict.get('chatroomname')
        content = json_dict.get('content')
        bot_username = json_dict.get('bot_username')

        # 如果是机器人发言
        if username == bot_username:
            return

        if msg_type != 'text' or not content:
            return

        zidou_bot = self.get_chatroom_zidou_bot(chatroomname, chatroom_zidou_account_dict)

        if username not in chatroom_member_info_dict.get(chatroomname, {}):
            chatroom_member_info_dict[chatroomname] = zidou_bot.get_member_info(chatroomname)
            if username not in chatroom_member_info_dict[chatroomname]:
                self.logger.warning(f'Failed processing msg {msg_id}: user {username} not found in {chatroomname}')
                return

        wechat_group_bot_config = self.get_wechat_group_bot_config(chatroomname)
        if wechat_group_bot_config['be_at']:
            bot_nickname = zidou_bot.nickname
            bot_be_at = f'@{bot_nickname}' in content
            if not bot_be_at:
                self.logger.info(f'Quit procssing msg {msg_id}: bot has not been @')
                return

            content = content.replace(f'@{bot_nickname}\u2005', '')
            content = content.replace(f'@{bot_nickname} ', '')
            if content.endswith(f'@{bot_nickname}'):
                content = content[:-len(f'@{bot_nickname}')]

        self.logger.info(f'Start requesting RSVP for msg {msg_id}, content: {content}')
        rsvp_group = Rsvp(
            self.conf['rsvp']['url'],
            wechat_group_bot_config['bot_id'],
            wechat_group_bot_config['share_token'],
            self.logger
        )

        ts = datetime.now()
        nick_name = chatroom_member_info_dict[chatroomname][username]['nickname']
        avatar_url = chatroom_member_info_dict[chatroomname][username]['avatar_url']
        user_id = ChatbotUserInfo.user_active_by_wechat(username, ts, nick_name, avatar_url)
        if not user_id:
            self.logger.warning(f'Failed processing msg {msg_id}: cannot get user_id for user {username}')
            return

        uid = f'openidgroup_{username}'
        try:
            resp = rsvp_group.get_bot_response(content, uid, wechat_group_bot_config['stage'])
        except Exception as e:
            import traceback
            self.logger.error(traceback.format_exc())
            resp = None

        if not resp:
            self.logger.warning(f'Failed to get rsvp response for msg {msg_id}, content: {content}')
            return
        self.logger.info(f'resp: {resp}')
        if resp.get('topic', 'fallback') != 'fallback' or wechat_group_bot_config['be_at']:
            similarity, bot_reply, start_miniprogram = self._parse_rsvp_response_stages(
                resp.get('stage', []),
                chatroomname,
                wechat_group_bot_config['be_at']
            )

            if bot_reply:
                zidou_bot.at_somebody(chatroomname, username, '', f'\n{bot_reply}')
            else:
                self.logger.warning(f'Failed to get bot reply for {msg_id}, content: {content}')

            if start_miniprogram:
                miniprogram_id_and_ts = zidou_bot.get_miniprogram_id_and_ts('棱小镜')
                if miniprogram_id_and_ts and not bot_reply:
                    zidou_bot.at_somebody(chatroomname, username, '', f'\n请打开下面小程序：')
                    zidou_bot.send_miniprogram_message(chatroomname, miniprogram_id_and_ts[0])
        else:
            bot_reply, similarity = '', 0
            bad_case = f'Bad case:\n{nick_name}: {content}'
            WxWorkNotification(self.logger).send(bad_case)

        bot_raw_reply = json.dumps(resp, ensure_ascii=False)
        save_chatbot_dialog(user_id, content, bot_reply, bot_raw_reply, similarity, ts, chatroomname)

    def send_msg(self, json_dict, chatroom_zidou_account_dict):
        if not json_dict:
            return
        self.logger.info(json_dict)

        msg_type = json_dict.get('type')
        chatroomname = json_dict.get('chatroomname')
        content = json_dict.get('content')
        if msg_type != 'text' or not content:
            self.logger.warning(f'Failed to send_msg, msg_type: {msg_type}, content: {content}')
            return

        zidou_bot = self.get_chatroom_zidou_bot(chatroomname, chatroom_zidou_account_dict)
        zidou_bot.send_text_message(chatroomname, content)

    def get_wechat_group_list(self, chatroom_member_info_dict, chatroom_zidou_account_dict):
        # TODO: cache for 1 min
        zidou_bot_dict = self.get_zidou_bot_dict()
        result = []
        for phone, zidou_bot in zidou_bot_dict.items():
            chatroom_list = zidou_bot.get_chatroom_list()
            for chatroom in chatroom_list:
                chatroomname = chatroom.get('chatroomname')
                roomowner = chatroom.get('roomowner')
                owner_nick_name = None
                owner_avatar_url = None
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

    # Helper functions
    def _parse_rsvp_response_stages(self, stages, wechat_group_id=None, be_at=0):
        # TODO: get similarity from stages
        similarity = None
        reply = ''
        start_miniprogram = False
        for stage in stages:
            if 'text' in stage:
                text = stage['text']
                for t in text.get('plainText', []):
                    if t == '您已经在小程序中...':
                        if wechat_group_id:
                            start_miniprogram = True
                        else:
                            t = '当前环境不支持小程序，或您已经在小程序中。'
                    else:
                        reply += t + '\n'
            if 'message' in stage:
                t = stage['message']
                if t == '您已经在小程序中...':
                    if wechat_group_id:
                        start_miniprogram = True
                    else:
                        t = '当前环境不支持小程序，或您已经在小程序中。'
                else:
                    reply += t + '\n'
            if 'link' in stage:
                link = stage['link']
                if 'text' in link:
                    reply +=  f'\n{link["text"]}：\n'
                if 'url' in link:
                    url = link['url']
                    if url.startswith('https://www.prism-advisor.com/'):
                        if wechat_group_id:
                            url = f'{url}&group={wechat_group_id}'
                        url = UrlManager.generate_short_url(url)
                    reply +=  f'{url}\n'
            if 'cards' in stage:
                cards = stage['cards']
                for card in cards.get('cards', []):
                    if 'title' in card:
                        reply += '\n' + card.get('title') + '\n'
                    replies = []
                    clicks = []
                    for button in card.get('buttons', []):
                        if 'postback' in button:
                            postback = button.get('postback')
                            if postback.startswith('https://www.prism-advisor.com/'):
                                if wechat_group_id:
                                    url  = f'{postback}&group={wechat_group_id}'
                                else:
                                    url = postback
                                clicks.append(f'{UrlManager.generate_short_url(url)}\n')
                            else:
                                replies.append(f'{postback}\n')
                    if clicks:
                        reply += '\n点击查看：\n'
                        for c in clicks:
                            reply += c
                    if replies:
                        if clicks:
                            if be_at:
                                reply += '\n您还可以@我之后说：\n'
                            else:
                                reply += '\n您还可以说：\n'
                        else:
                            if be_at:
                                reply += '\n您可以@我之后说：\n'
                            else:
                                reply += '\n您可以说：\n'
                        for r in replies:
                            reply += r
            if 'list' in stage:
                list_stage = stage['list']
                for item in list_stage.get('items', []):
                    if 'title' in item:
                        reply += '\n' + item.get('title') + '\n'
                    replies = []
                    clicks = []
                    for button in item.get('buttons', []):
                        if 'postback' in button:
                            postback = button.get('postback')
                            if postback.startswith('https://www.prism-advisor.com/'):
                                if wechat_group_id:
                                    url  = f'{postback}&group={wechat_group_id}'
                                else:
                                    url = postback
                                clicks.append(f'{UrlManager.generate_short_url(url)}\n')
                            else:
                                replies.append(f'{postback}\n')
                    if clicks:
                        reply += '\n点击查看：\n'
                        for c in clicks:
                            reply += c
                    if replies:
                        if clicks:
                            if be_at:
                                reply += '\n您还可以@我之后说：\n'
                            else:
                                reply += '\n您还可以说：\n'
                        else:
                            if be_at:
                                reply += '\n您可以@我之后说：\n'
                            else:
                                reply += '\n您可以说：\n'
                        for r in replies:
                            reply += r
            if 'quickReplies' in stage:
                quick_replies = stage['quickReplies']
                if 'quickReplies' in quick_replies:
                    quick_replies = quick_replies['quickReplies']
                    if be_at:
                        reply += '—————————————\n您可以@我之后说：\n'
                    else:
                        reply += '—————————————\n您可以说：\n'
                    for quick_reply in quick_replies:
                        reply += f'{quick_reply["postback"]}\n'

        return similarity, reply, start_miniprogram

