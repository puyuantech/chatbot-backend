
from flask import Blueprint
from flask_restful import Api

from .view import WXPublicAccountAPI, WXArticleAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/search')
api = Api(blu)

api.add_resource(WXPublicAccountAPI, '/wx_pa/<string:key_word>')
api.add_resource(WXArticleAPI, '/wx_article/<string:key_word>')

