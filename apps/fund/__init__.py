
from flask import Blueprint
from flask_restful import Api

from .view_funds import FundInfoAPI, FundInfosAPI
from .view_pools import FundPoolAPI, FundPoolsAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/fund')
api = Api(blu)

api.add_resource(FundInfoAPI, '/info')
api.add_resource(FundInfosAPI, '/info/list')

api.add_resource(FundPoolAPI, '/pool')
api.add_resource(FundPoolsAPI, '/pool/list')

