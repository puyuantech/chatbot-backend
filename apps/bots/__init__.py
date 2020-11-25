from flask import Blueprint
from .view import api


blu = Blueprint('{}_blu'.format(__name__), __name__)
api.register(blu)

