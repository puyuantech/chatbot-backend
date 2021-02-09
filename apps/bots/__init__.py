
import traceback

from flask import Blueprint, current_app
from flask_restful import Api

from bases.exceptions import BaseError
from utils.helper import ERROR_RSP

from .view_prism import api as prism_api

from .view_chats import GroupListAPI, GroupBotConfigAPI, ChatBotInfoAPI, ChatFromMiniAPI, ChatFromWechatAPI
from .view_cognai import CognaiDialogAPI
from .view_dialogs import DialogsByTagAPI, DialogsByUserAPI, DialogsByWechatAPI
from .view_messages import TextMessageAPI, LinkMessageAPI, PicMessageAPI, MessageHistoryAPI
from .view_statistics import (ExpertiseDistributionAPI, RiskToleranceDistributionAPI, DialogCountDistributionAPI,
                              ProductViewCountAPI, UserCountAPI, DialogCountAPI, ProductDailyViewAPI)
from .view_tags import TagsAPI, TopTagsAPI, TagAPI
from .view_users import UserInfoAPI, UserListAPI, UserTagAPI, UserProductViewAPI

blu = Blueprint('{}_blu'.format(__name__), __name__)
api = Api(blu)

api.add_resource(GroupListAPI, '/api/v1/chatbot/wechat_group/list')
api.add_resource(GroupBotConfigAPI, '/api/v1/chatbot/wechat_group/bot_config')
api.add_resource(ChatBotInfoAPI, '/api/v1/chatbot/bot_info')
api.add_resource(ChatFromMiniAPI, '/api/v1/chatbot/chat')
api.add_resource(ChatFromWechatAPI, '/api/v1/chatbot/wechat_group/chatroom_msg_callback')

api.add_resource(CognaiDialogAPI, '/api/v1/chatbot/cognai/dialog')

api.add_resource(DialogsByTagAPI, '/api/v1/chatbot/dialogs/tag')
api.add_resource(DialogsByUserAPI, '/api/v1/chatbot/user/dialog')
api.add_resource(DialogsByWechatAPI, '/api/v1/chatbot/wechat_group/dialog')

api.add_resource(TextMessageAPI, '/api/v1/chatbot/wechat_group/send_text_msg')
api.add_resource(LinkMessageAPI, '/api/v1/chatbot/wechat_group/send_link_msg')
api.add_resource(PicMessageAPI, '/api/v1/chatbot/wechat_group/send_pic_msg')
api.add_resource(MessageHistoryAPI, '/api/v1/chatbot/wechat_group/msg_history')

api.add_resource(ExpertiseDistributionAPI, '/api/v1/chatbot/statistics/user_expertise')
api.add_resource(RiskToleranceDistributionAPI, '/api/v1/chatbot/statistics/user_risk_tolerance')
api.add_resource(DialogCountDistributionAPI, '/api/v1/chatbot/statistics/user_dialog_count')
api.add_resource(ProductViewCountAPI, '/api/v1/chatbot/statistics/product_view_count')
api.add_resource(UserCountAPI, '/api/v1/chatbot/statistics/user_count')
api.add_resource(DialogCountAPI, '/api/v1/chatbot/statistics/dialog_count')
api.add_resource(ProductDailyViewAPI, '/api/v1/chatbot/statistics/product_daily_view')

api.add_resource(TagsAPI, '/api/v1/chatbot/tags')
api.add_resource(TopTagsAPI, '/api/v1/chatbot/tags/top')
api.add_resource(TagAPI, '/api/v1/chatbot/tag')

api.add_resource(UserInfoAPI, '/api/v1/chatbot/user/info')
api.add_resource(UserListAPI, '/api/v1/chatbot/user/list')
api.add_resource(UserTagAPI, '/api/v1/chatbot/user/tag')
api.add_resource(UserProductViewAPI, '/api/v1/chatbot/user/product_view')

prism_api.register(blu)


@blu.errorhandler(Exception)
def _handle_exception(e):
    """错误处理"""
    current_app.logger.error(e)
    current_app.logger.error(traceback.format_exc())
    if isinstance(e, BaseError):
        return ERROR_RSP('', e.msg, e.code, e.status)
    return ERROR_RSP('server error', 'server error', 1005, 500)

