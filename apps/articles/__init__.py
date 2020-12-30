
from flask import Blueprint
from flask_restful import Api

from .view import ArticleAPI, ArticleCountAPI, PublicAccountAPI, PublicAccountListAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1')
api = Api(blu)

api.add_resource(ArticleCountAPI, '/article/count')
api.add_resource(ArticleAPI, '/article/list')

api.add_resource(PublicAccountListAPI, '/public_account/list')
api.add_resource(PublicAccountAPI, '/public_account/detail')
