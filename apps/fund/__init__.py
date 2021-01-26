
from flask import Blueprint
from flask_restful import Api

from .view_funds import FundInfoAPI, FundInfosAPI, FundInfosPaginationAPI
from .view_managers import FundManagerAPI, FundManagersAPI, FundManagerInfosAPI
from .view_pools import FundPoolAPI, FundPoolsAPI
from .view_recommend import (FundRecommendMenuAPI, FundRecommendBySectorAPI, FundRecommendByAbilityAPI,
                             FundRecommendByFundTypeAPI, FundRecommendByPreferenceAPI, FundRecommendByIndexAPI,
                             FundRecommendByBenchmarkAPI, FundRecommendByHoldStockAPI, FundRecommendByHoldBondAPI,
                             FundRecommendByETFAPI, FundRecommendByKeyAPI)
from .view_sectors import SectorNameAPI, SectorInfoAPI, SectorInfosAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/fund')
api = Api(blu)

api.add_resource(FundInfoAPI, '/info')
api.add_resource(FundInfosAPI, '/info/list')
api.add_resource(FundInfosPaginationAPI, '/info/pagination')

api.add_resource(FundManagerAPI, '/manager')
api.add_resource(FundManagersAPI, '/manager/list')
api.add_resource(FundManagerInfosAPI, '/manager/info')

api.add_resource(FundPoolAPI, '/pool')
api.add_resource(FundPoolsAPI, '/pool/list')

api.add_resource(FundRecommendMenuAPI, '/recommend/menu')
api.add_resource(FundRecommendBySectorAPI, '/recommend/sector')
api.add_resource(FundRecommendByAbilityAPI, '/recommend/ability')
api.add_resource(FundRecommendByFundTypeAPI, '/recommend/fund_type')
api.add_resource(FundRecommendByPreferenceAPI, '/recommend/preference')
api.add_resource(FundRecommendByIndexAPI, '/recommend/index')
api.add_resource(FundRecommendByBenchmarkAPI, '/recommend/benchmark')
api.add_resource(FundRecommendByHoldStockAPI, '/recommend/hold_stock')
api.add_resource(FundRecommendByHoldBondAPI, '/recommend/hold_bond')
api.add_resource(FundRecommendByETFAPI, '/recommend/etf')
api.add_resource(FundRecommendByKeyAPI, '/recommend/key')

api.add_resource(SectorNameAPI, '/sector/name')
api.add_resource(SectorInfoAPI, '/sector/info')
api.add_resource(SectorInfosAPI, '/sector/info/list')
