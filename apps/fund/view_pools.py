
from bases.exceptions import LogicError, ParamsError
from bases.globals import db
from bases.viewhandler import ApiViewHandler
from models import FundPool
from utils.decorators import login_required, params_required, permission_required

from .constants import PoolType


class FundPoolAPI(ApiViewHandler):

    @login_required
    @permission_required('基金管理')
    @params_required(*['fund_id', 'pool_type'])
    def post(self):
        if self.input.pool_type not in PoolType.get_codes():
            raise ParamsError('未知参数: (pool_type){}'.format(self.input.pool_type))

        if FundPool.filter_by_query(
            fund_id=self.input.fund_id,
            pool_type=self.input.pool_type,
        ).one_or_none():
            raise LogicError('基金已存在！')

        FundPool.create(
            fund_id=self.input.fund_id,
            pool_type=self.input.pool_type,
        )
        return 'success'

    @login_required
    @permission_required('基金管理')
    @params_required(*['fund_id', 'pool_type'])
    def delete(self):
        if self.input.pool_type not in PoolType.get_codes():
            raise ParamsError('未知参数: (pool_type){}'.format(self.input.pool_type))

        fund = FundPool.get_by_query(self.input.tag_id)
        fund.logic_delete()
        return 'success'


class FundPoolsAPI(ApiViewHandler):

    @login_required
    @permission_required('基金管理')
    @params_required(*['pool_type'])
    def get(self):
        if self.input.pool_type not in PoolType.get_codes():
            raise ParamsError('未知参数: (pool_type){}'.format(self.input.pool_type))

        fund_ids = FundPool.get_fund_ids(self.input.pool_type)
        return {'fund_ids': fund_ids}

    @login_required
    @permission_required('基金管理')
    @params_required(*['fund_ids', 'pool_type'])
    def post(self):
        if self.input.pool_type not in PoolType.get_codes():
            raise ParamsError('未知参数: (pool_type){}'.format(self.input.pool_type))

        fund_ids = FundPool.get_fund_ids(self.input.pool_type)

        for fund_id in self.input.fund_ids:
            if fund_id in fund_ids:
                continue

            FundPool(
                fund_id=fund_id,
                pool_type=self.input.pool_type,
            ).save(commit=False)

        db.session.commit()
        return 'success'

    @login_required
    @permission_required('基金管理')
    @params_required(*['fund_ids', 'pool_type'])
    def delete(self):
        if self.input.pool_type not in PoolType.get_codes():
            raise ParamsError('未知参数: (pool_type){}'.format(self.input.pool_type))

        FundPool.delete_fund_ids(self.input.fund_ids, self.input.pool_type)
        return 'success'

