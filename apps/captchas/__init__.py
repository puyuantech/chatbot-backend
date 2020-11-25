from flask import Blueprint
from flask_restful import Api
from .view import GetCaptcha, CaptchaCheckAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/captcha')
api = Api(blu)

api.add_resource(GetCaptcha, '/generate')
api.add_resource(CaptchaCheckAPI, '/check')

