
from flask import Blueprint
from flask_restful import Api

from .view_funds import FundInfoAPI, FundInfosAPI
from .view_managers import FundManagerAPI, FundManagersAPI
from .view_pools import FundPoolAPI, FundPoolsAPI
from .view_sectors import SectorNameAPI, SectorInfoAPI, SectorInfosAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/fund')
api = Api(blu)

api.add_resource(FundInfoAPI, '/info')
api.add_resource(FundInfosAPI, '/info/list')

api.add_resource(FundManagerAPI, '/manager')
api.add_resource(FundManagersAPI, '/manager/list')

api.add_resource(FundPoolAPI, '/pool')
api.add_resource(FundPoolsAPI, '/pool/list')

api.add_resource(SectorNameAPI, '/sector/name')
api.add_resource(SectorInfoAPI, '/sector/info')
api.add_resource(SectorInfosAPI, '/sector/info/list')
