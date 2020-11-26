import traceback
from flask import Blueprint, current_app
from bases.exceptions import BaseError
from utils.helper import ERROR_RSP
from .view import api
from .view_prism import api as prism_api


blu = Blueprint('{}_blu'.format(__name__), __name__)
api.register(blu)
prism_api.register(blu)


@blu.errorhandler(Exception)
def _handle_exception(e):
    """错误处理"""
    current_app.logger.error(traceback.format_exc)
    if isinstance(e, BaseError):
        return ERROR_RSP('', e.msg, e.code, e.status)
    return ERROR_RSP('server error', 'server error', 1005, 500)

