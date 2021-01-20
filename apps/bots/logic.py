import json
from datetime import datetime, timedelta
from sqlalchemy import func, text

from bases.globals import settings, db
from models import (
    ChatbotDialog,
    ChatbotDialogStat,
    ChatbotProductView,
    ChatbotUserInfo,
    ChatbotUserStat,
    ChatbotProductDailyView,
    WechatGroupBotConfig
)
from extensions.rsvp import Rsvp
from extensions.zidou import ZiDou
from extensions.cognai import Cognai
from extensions.url_manager import UrlManager
from extensions.wxwork import WxWorkNotification
from .constants import Operation, TagType
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
        q = db.session.query(
            ChatbotDialogStat.user_id,
            func.sum(ChatbotDialogStat.dialog_count).label('total'),
        ).group_by(
            ChatbotDialogStat.user_id,
        ).order_by(
            text('total DESC')
        )
        if wechat_group_id:
            q = q.filter(ChatbotDialogStat.wechat_group_id == wechat_group_id)
        if top_n:
            q = q.limit(top_n)
        all_user_stats = q.all()

        user_dialog_count = {}
        for user_id, dialog_count in all_user_stats:
            user_dialog_count[user_id] = dialog_count

        result = []
        if not user_dialog_count:
            return result

        q = db.session.query(
            ChatbotUserInfo
        )
        if wechat_group_id or top_n:
            q = q.filter(ChatbotUserInfo.id.in_(user_dialog_count.keys()))
        all_user_info = q.all()
        for user in all_user_info:
            user_dict = user.to_dict(remove_fields_list=['update_time'])
            user_dict['source'] = '微信群' if user_dict.pop('wechat_user_name') else '小程序'
            user_dict['user_id'] = user_dict.pop('id')
            user_dict.update({
                "dialog_count": int(user_dialog_count.get(user.id, 0))
            })
            result.append(user_dict)

        if top_n:
            result.sort(key=lambda item: item['dialog_count'], reverse=True)

        return result

    def get_user_info(self, user_id=None, rsvp_user_id=None):
        if not user_id:
            user_id = self._get_user_from_rsvp_id(rsvp_user_id, datetime.now())
        user = db.session.query(
            ChatbotUserInfo
        ).filter(
            ChatbotUserInfo.id == user_id
        ).one_or_none()
        if not user:
            return {}

        user_dialog_count = db.session.query(
            func.sum(ChatbotDialogStat.dialog_count),
        ).filter(
            ChatbotDialogStat.user_id == user_id
        ).one_or_none()

        user_dict = user.to_dict(remove_fields_list=['update_time'])
        user_dict['source'] = '微信群' if user_dict.pop('wechat_user_name') else '小程序'
        user_dict['user_id'] = user_dict.pop('id')
        user_dict.update({
            "dialog_count": int(user_dialog_count[0]) if user_dialog_count[0] else 0
        })

        return user_dict

    def get_user_dialog(self, user_id, start=None, end=None):
        q = db.session.query(
            ChatbotDialog
        ).filter(
            ChatbotDialog.user_id == user_id
        ).order_by(
            text('ts DESC')
        )
        if start:
            q = q.filter(ChatbotDialog.ts >= start)
        if end:
            q = q.filter(ChatbotDialog.ts <= end)
        dialogs = q.all()
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
        users = db.session.query(
            ChatbotUserInfo
        ).all()
        for user in users:
            user_info_dict[user.id] = {
                'nick_name': user.nick_name,
                'head_img': user.head_img
            }

        q = db.session.query(
            ChatbotDialog
        ).filter(
            ChatbotDialog.wechat_group_id == wechat_group_id
        ).order_by(
            text('ts DESC')
        )
        if start:
            q = q.filter(ChatbotDialog.ts >= start)
        if end:
            q = q.filter(ChatbotDialog.ts <= end)
        dialogs = q.all()
        result = []
        for dialog in dialogs:
            dialog_dict = dialog.to_dict(remove_fields_list=['create_time', 'update_time'])
            dialog_dict['nickname'] = user_info_dict.get(dialog_dict['user_id'], {}).get('nick_name')
            dialog_dict['head_img'] = user_info_dict.get(dialog_dict['user_id'], {}).get('head_img')
            dialog_dict['tags'] = get_tags_by_dialog_id(dialog.id)

            result.append(dialog_dict)
        return result

    def get_wechat_group_bot_config(self, wechat_group_id):
        bot_config = db.session.query(
            WechatGroupBotConfig
        ).filter_by(
            wechat_group_id=wechat_group_id,
        ).one_or_none()

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

    def set_wechat_group_bot_config(self, wechat_group_id, bot_id, share_token, stage, be_at):
        bot_config = db.session.query(
            WechatGroupBotConfig
        ).filter_by(
            wechat_group_id=wechat_group_id,
        ).one_or_none()

        if not stage:
            stage = 'release'

        if not be_at:
            be_at = 0

        if not bot_config:
            bot_config = WechatGroupBotConfig(
                wechat_group_id = wechat_group_id,
                bot_id = bot_id,
                share_token = share_token,
                stage = stage,
                be_at = be_at
            )
            db.session.add(bot_config)
        else:
            bot_config.bot_id = bot_id
            bot_config.share_token = share_token
            bot_config.stage = stage
            bot_config.be_at = be_at

        db.session.commit()

    def get_user_count(self, start=None, end=None, wechat_group_id=None):
        q = db.session.query(
            ChatbotUserStat
        )
        if start:
            start = datetime.fromisoformat(start)
            q = q.filter(ChatbotUserStat.ts >= start - timedelta(days=1))
        if end:
            end = datetime.fromisoformat(end)
            q = q.filter(ChatbotUserStat.ts <= end)
        user_counts = q.all()

        min_ts = start
        max_ts = end
        user_count_dict = {}
        active_user_count_dict = {}
        for item in user_counts:
            if not min_ts or min_ts > item.ts:
                min_ts = item.ts
            if not max_ts or max_ts < item.ts:
                max_ts = item.ts
            user_count_dict[item.ts] = int(item.user_count)
            active_user_count_dict[item.ts] = int(item.active_user_count)

        ts_list = []
        user_count_list = []
        new_user_count_list = []
        active_user_count_list = []
        cur_ts = min_ts
        last_user_count = 0
        if min_ts and max_ts:
            if not start or min_ts == start:
                last_user_count = 0
            else:
                cur_ts = start
            while cur_ts <= max_ts:
                ts_list.append(cur_ts)
                yesterday = cur_ts - timedelta(days=1)
                user_count = max(user_count_dict.get(cur_ts, 0), last_user_count)
                user_count_list.append(user_count)
                new_user_count_list.append(user_count - last_user_count)
                active_user_count_list.append(active_user_count_dict.get(cur_ts, 0))
                last_user_count = user_count
                cur_ts += timedelta(days=1)

        return {
            'ts': ts_list,
            'user_count': user_count_list,
            'new_user_count': new_user_count_list,
            'active_user_count': active_user_count_list
        }

    def get_user_expertise(self):
        result = {}
        expertise_levels = ['低', '较低', '中等', '较高', '高']
        for level in expertise_levels:
            result[level] = 0

        users = db.session.query(
            ChatbotUserInfo
        ).all()

        for user in users:
            user_expertise = ChatbotUserInfo.readable_expertise(user)
            result[user_expertise] += 1

        return result

    def get_user_risk_tolerance(self):
        result = {}
        risk_tolerance_levels = ['安逸型', '保守型', '稳健型', '积极型', '进取型']
        for level in risk_tolerance_levels:
            result[level] = 0

        users = db.session.query(
            ChatbotUserInfo
        ).all()

        for user in users:
            user_risk_tolerance = ChatbotUserInfo.readable_risk_tolerance(user)
            result[user_risk_tolerance] += 1

        return result

    def get_user_dialog_count(self):
        result = {}
        dialog_count_levels = ['[0, 10]', '(10, 100]', '(100, 1000]', '(1000, max]']
        for level in dialog_count_levels:
            result[level] = 0

        dialog_counts = db.session.query(
            func.sum(ChatbotDialogStat.dialog_count),
        ).group_by(
            ChatbotDialogStat.user_id
        ).all()

        for dialog_count, in dialog_counts:
            if dialog_count < 10:
                result['[0, 10]'] += 1
            elif dialog_count < 100:
                result['(10, 100]'] += 1
            elif dialog_count < 1000:
                result['(100, 1000]'] += 1
            else:
                result['(1000, max]'] += 1

        return result

    def get_dialog_count(self, user_id=None, start=None, end=None):
        q = db.session.query(
            ChatbotDialogStat.ts,
            func.sum(ChatbotDialogStat.dialog_count),
        ).group_by(
            ChatbotDialogStat.ts,
        )
        if user_id:
            q = q.filter(ChatbotDialogStat.user_id == user_id)
        if start:
            q = q.filter(ChatbotDialogStat.ts >= start)
        if end:
            q = q.filter(ChatbotDialogStat.ts <= end)

        dialog_counts = q.all()

        min_ts = datetime.fromisoformat(start) if start else None
        max_ts = datetime.fromisoformat(end) if end else None
        dialog_count_dict = {}
        for ts, dialog_count in dialog_counts:
            if not min_ts or min_ts > ts:
                min_ts = ts
            if not max_ts or max_ts < ts:
                max_ts = ts
            dialog_count_dict[ts] = int(dialog_count)

        ts_list = []
        dialog_count_list = []
        cur_ts = min_ts
        if min_ts and max_ts:
            while cur_ts <= max_ts:
                ts_list.append(cur_ts)
                dialog_count_list.append(dialog_count_dict.get(cur_ts, 0))
                cur_ts += timedelta(days=1)

        return {
            'ts': ts_list,
            'dialog_count': dialog_count_list
        }

    def get_product_view_count(self, user_id=None, wechat_group_id=None, start=None, end=None, top_n=None):
        q = db.session.query(
            ChatbotProductView.product_id,
            ChatbotProductView.product_type,
            ChatbotProductView.product_name,
            func.count('*').label('total'),
        ).group_by(
            ChatbotProductView.product_id,
            ChatbotProductView.product_type,
        ).order_by(
            text('total DESC')
        )

        if user_id:
            q = q.filter(ChatbotProductView.user_id == user_id)
        if wechat_group_id:
            q = q.filter(ChatbotProductView.wechat_group_id == wechat_group_id)
        if start:
            q = q.filter(ChatbotProductView.ts >= start)
        if end:
            q = q.filter(ChatbotProductView.ts <= end)

        if top_n:
            q = q.limit(top_n)
        product_view_counts = q.all()

        result = []
        for product_id, product_type, product_name, product_view_count in product_view_counts:
            result.append({
                'product_id': product_id,
                'product_type': product_type,
                'product_name': product_name,
                'product_view_count': product_view_count
            })

        return result

    def get_product_daily_view(self, user_id=None, start=None, end=None):
        q = db.session.query(
            ChatbotProductDailyView.ts,
            func.sum(ChatbotProductDailyView.product_view_count),
        ).group_by(
            ChatbotProductDailyView.ts,
        )
        if user_id:
            q = q.filter(ChatbotProductDailyView.user_id == user_id)
        if start:
            q = q.filter(ChatbotProductDailyView.ts >= start)
        if end:
            q = q.filter(ChatbotProductDailyView.ts <= end)

        product_view_counts = q.all()

        min_ts = datetime.fromisoformat(start) if start else None
        max_ts = datetime.fromisoformat(end) if end else None
        product_view_count_dict = {}
        for ts, product_view_count in product_view_counts:
            if not min_ts or min_ts > ts:
                min_ts = ts
            if not max_ts or max_ts < ts:
                max_ts = ts
            product_view_count_dict[ts] = int(product_view_count)

        ts_list = []
        product_view_count_list = []
        cur_ts = min_ts
        if min_ts and max_ts:
            while cur_ts <= max_ts:
                ts_list.append(cur_ts)
                product_view_count_list.append(product_view_count_dict.get(cur_ts, 0))
                cur_ts += timedelta(days=1)

        return {
            'ts': ts_list,
            'product_view_count': product_view_count_list
        }

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

        user_id = self._get_user_from_rsvp_id(req.get('uid'), ts)
        if not user_id:
            return

        user_input = req.get('question')
        similarity, bot_reply, start_miniprogram = self._parse_rsvp_response_stages(resp.get('stage', []))

        bot_raw_reply = json.dumps(resp, ensure_ascii=False)

        chatbot_dialog = ChatbotDialog(
            user_id=user_id,
            user_input=user_input,
            bot_reply=bot_reply,
            bot_raw_reply=bot_raw_reply,
            similarity=similarity,
            ts=ts
        )
        db.session.add(chatbot_dialog)
        db.session.commit()

        self._update_dialog_stat(user_id, ts.date())
        self._update_user_stat(ts.date())

    def update_user_tag(self, rsvp_user_id, tag_type, tag_value, operation):
        user_id = self._get_user_from_rsvp_id(rsvp_user_id, datetime.now())
        if not user_id:
            return

        chatbot_user = db.session.query(
            ChatbotUserInfo
        ).filter_by(
            id=user_id,
        ).one_or_none()
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

        user_id = self._get_user_from_rsvp_id(rsvp_user_id, ts)
        if not user_id:
            return

        user_product_view = ChatbotProductView(
            user_id=user_id,
            product_id=product_id,
            product_type=product_type,
            product_name=product_name,
            ts=ts
        )
        if wechat_group_id:
            user_product_view.wechat_group_id = wechat_group_id

        db.session.add(user_product_view)
        db.session.commit()

        # Update product view statistics
        self._update_product_stat(user_id, wechat_group_id, ts.date())

    def get_rsvp_bot(self):
        rsvp_conf = self.conf['rsvp']
        return Rsvp(rsvp_conf['url'], rsvp_conf['bot_id'], rsvp_conf['share_token'], self.logger)

    def get_bot_info(self):
        rsvp_bot = self.get_rsvp_bot()
        resp = rsvp_bot.get_bot_info()
        return resp

    def chat(self, json_dict):
        if not json_dict:
            return None
        query = json_dict.get('query')
        user_id = json_dict.get('user_id')
        if not query or not user_id:
            return None
        user_id = str(user_id)

        ts = datetime.now()
        uid = f'openidprism_{user_id}'
        rsvp_bot = self.get_rsvp_bot()
        resp = rsvp_bot.get_bot_response(query, uid)
        if not resp:
            return None
        similarity, bot_reply, start_miniprogram = self._parse_rsvp_response_stages(resp.get('stage', []))
        bot_raw_reply = json.dumps(resp, ensure_ascii=False)

        chatbot_dialog = ChatbotDialog(
            user_id=user_id,
            user_input=query,
            bot_reply=bot_reply,
            bot_raw_reply=bot_raw_reply,
            similarity=similarity,
            ts=ts
        )
        db.session.add(chatbot_dialog)
        db.session.commit()

        self._update_dialog_stat(user_id, ts.date())
        self._update_user_stat(ts.date())

        return resp

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

        time = json_dict.get('time')
        msg_id = json_dict.get('msg_id')
        username = json_dict.get('username')
        msg_type = json_dict.get('type')
        chatroomname = json_dict.get('chatroomname')
        content = json_dict.get('content')
        bot_username = json_dict.get('bot_username')
        is_at = json_dict.get('is_at')
        be_at_list = json_dict.get('be_at_list')

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
            # if not is_at:
            #     self.logger.info(f'Quit procssing msg {msg_id}: bot is not @ed')
            #     return
            # bot_be_at = False
            # for be_at in be_at_list:
            #     if be_at == bot_username:
            #         bot_be_at = True
            #         break
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
        user_id = self._get_user(ts, wechat_user_name=username, nick_name=nick_name, avatar_url=avatar_url)
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
            bot_reply = ''
            similarity = 0
            reporter = WxWorkNotification(self.logger)
            bad_case = f'Bad case:\n{nick_name}: {content}'
            reporter.send(bad_case)

        bot_raw_reply = json.dumps(resp, ensure_ascii=False)

        chatbot_dialog = ChatbotDialog(
            user_id=user_id,
            user_input=content,
            bot_reply=bot_reply,
            bot_raw_reply=bot_raw_reply,
            similarity=similarity,
            ts=ts,
            wechat_group_id=chatroomname
        )
        db.session.add(chatbot_dialog)
        db.session.commit()

        self._update_dialog_stat(user_id, ts.date(), chatroomname)
        self._update_user_stat(ts.date())

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

    def _get_user_from_rsvp_id(self, rsvp_user_id, ts):
        if len(rsvp_user_id) <= 12:
            return None

        source = rsvp_user_id[6:12]
        user_id = None
        wechat_user_name = None
        if source == 'prism_':
            user_id = rsvp_user_id[12:]
        elif source == 'group_':
            wechat_user_name = rsvp_user_id[12:]
        else:
            return None

        return self._get_user(ts, user_id=user_id, wechat_user_name=wechat_user_name)

    def _get_user(self, ts, user_id=None, wechat_user_name=None, nick_name=None, avatar_url=None):
        if not user_id and not wechat_user_name:
            self.logger.error('One of user_id and wechat_user_name must exists')
            return None

        if user_id:
                user = db.session.query(ChatbotUserInfo).filter_by(
                    id=user_id,
                ).one_or_none()
                if not user:
                    self.logger.error(f'Cannot find user with ID {user_id}')
                    return None

                user.last_action_ts = ts
                db.session.commit()

                return user.id
        else:
            chatbot_user = db.session.query(
                ChatbotUserInfo
            ).filter_by(
                wechat_user_name=wechat_user_name,
            ).one_or_none()
            if not chatbot_user:
                chatbot_user = ChatbotUserInfo(
                    create_time=ts,
                    wechat_user_name=wechat_user_name,
                    nick_name=nick_name,
                    head_img=avatar_url,
                    last_action_ts=ts,
                    expertise=0,
                    risk_tolerance=0
                )
                db.session.add(chatbot_user)
            else:
                chatbot_user.last_action_ts = ts
                db.session.commit()

                return chatbot_user.id

    def _update_dialog_stat(self, user_id, ts, wechat_group_id=None):
        query = db.session.query(
            ChatbotDialogStat
        ).filter_by(
            user_id=user_id,
            ts=ts,
        )
        if wechat_group_id:
            query = query.filter_by(
                wechat_group_id=wechat_group_id
            )
        chatbot_dialog_count = query.one_or_none()
        if not chatbot_dialog_count:
            chatbot_dialog_count = ChatbotDialogStat(
                dialog_count=1,
                user_id=user_id,
                ts=ts,
            )
            if wechat_group_id:
                chatbot_dialog_count.wechat_group_id = wechat_group_id
            db.session.add(chatbot_dialog_count)
        else:
            chatbot_dialog_count.dialog_count += 1

            db.session.commit()

    def _update_user_stat(self, ts):
        chatbot_user_stat = db.session.query(
            ChatbotUserStat
        ).filter_by(
            ts=ts
        ).one_or_none()

        if not chatbot_user_stat:
            chatbot_user_stat = ChatbotUserStat(
                ts=ts,
            )
            db.session.add(chatbot_user_stat)

        # Total user count
        user_count = db.session.query(
            func.count(ChatbotUserInfo.id),
        ).one_or_none()[0]

        # Active user count
        active_user_count = db.session.query(
            func.count(ChatbotUserInfo.id),
        ).filter(
            ChatbotUserInfo.is_deleted == False,
            ChatbotUserInfo.last_action_ts >= ts
        ).one_or_none()[0]

        chatbot_user_stat.user_count = user_count
        chatbot_user_stat.active_user_count = active_user_count

        db.session.commit()

    def _update_product_stat(self, user_id, wechat_group_id, ts):
        query = db.session.query(
            ChatbotProductDailyView
        ).filter_by(
            user_id=user_id,
            ts=ts,
        )
        if wechat_group_id:
            query = query.filter(ChatbotProductDailyView.wechat_group_id == wechat_group_id)

        chatbot_product_daily_view = query.one_or_none()
        if not chatbot_product_daily_view:
            chatbot_product_daily_view = ChatbotProductDailyView(
                product_view_count=1,
                user_id=user_id,
                ts=ts,
            )
            if wechat_group_id:
                chatbot_product_daily_view.wechat_group_id = wechat_group_id
            db.session.add(chatbot_product_daily_view)
        else:
            chatbot_product_daily_view.product_view_count += 1

        db.session.commit()

