from flask import Blueprint
from .view import api


blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1')
api.register(blu)

