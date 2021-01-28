import traceback
from flask import Blueprint, current_app
from flask_restful import Api
from bases.exceptions import BaseError
from utils.helper import ERROR_RSP
from .view import api as view_api
from .view_dialogs import DialogsByTagAPI
from .view_prism import api as prism_api
from .view_statistics import (ExpertiseDistributionAPI, RiskToleranceDistributionAPI, DialogCountDistributionAPI,
                              ProductViewCountAPI, UserCountAPI, DialogCountAPI, ProductDailyViewAPI)
from .view_tags import TagsAPI, TopTagsAPI, TagAPI

blu = Blueprint('{}_blu'.format(__name__), __name__)
api = Api(blu)

api.add_resource(DialogsByTagAPI, '/api/v1/chatbot/dialogs/tag')

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

view_api.register(blu)
prism_api.register(blu)


@blu.errorhandler(Exception)
def _handle_exception(e):
    """错误处理"""
    current_app.logger.error(e)
    current_app.logger.error(traceback.format_exc())
    if isinstance(e, BaseError):
        return ERROR_RSP('', e.msg, e.code, e.status)
    return ERROR_RSP('server error', 'server error', 1005, 500)

