from flask import Blueprint
from flask_restful import Api
from .view import ResetPassword, ChangeAPI, SelfPermission, UpLoadHeadImg

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/accounts')
api = Api(blu)

api.add_resource(ResetPassword, '/reset_password')
api.add_resource(ChangeAPI, '/change')
api.add_resource(SelfPermission, '/self_permission')
api.add_resource(UpLoadHeadImg, '/avatar')

