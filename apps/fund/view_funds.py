
from flask import g

from bases.exceptions import BaseError, ParamsError
from bases.viewhandler import ApiViewHandler
from extensions.robo import Robo
from models import FundPool
from utils.decorators import login_required, params_required

from .constants import PoolType


class FundInfoAPI(ApiViewHandler):

    @login_required
    @params_required(*['fund_id'])
    def get(self):
        fund_info = Robo.get_fund_info([self.input.fund_id], g.user.id)
        if len(fund_info) == 0:
            raise BaseError('基金不存在!')

        return {'data': fund_info[0]}


class FundInfosAPI(ApiViewHandler):

    @login_required
    @params_required(*['pool_type'])
    def get(self):
        if self.input.pool_type not in PoolType.get_codes():
            raise ParamsError('未知参数: (pool_type){}'.format(self.input.pool_type))

        fund_ids = FundPool.get_fund_ids(self.input.pool_type)
        fund_info = Robo.get_fund_info(fund_ids, g.user.id)
        return {'data': fund_info}

    @login_required
    @params_required(*['fund_ids'])
    def post(self):
        if not isinstance(self.input.fund_ids, list):
            raise ParamsError('fund_ids 参数类型错误: (type){}'.format(type(self.input.fund_ids)))

        fund_info = Robo.get_fund_info(self.input.fund_ids, g.user.id)
        return {'data': fund_info}

