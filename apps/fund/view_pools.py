
from bases.viewhandler import ApiViewHandler
from models import FundPool
from utils.decorators import login_required, params_required, permission_required

from .libs.pools import check_pool_type_valid


class FundPoolAPI(ApiViewHandler):

    @login_required
    @permission_required('基金管理')
    @params_required(*['fund_id', 'pool_type'])
    @check_pool_type_valid
    def post(self):
        FundPool.add_fund_id(self.input.fund_id, self.input.pool_type)
        return 'success'

    @login_required
    @permission_required('基金管理')
    @params_required(*['fund_id', 'pool_type'])
    @check_pool_type_valid
    def delete(self):
        FundPool.delete_fund_id(self.input.fund_id, self.input.pool_type)
        return 'success'


class FundPoolsAPI(ApiViewHandler):

    @login_required
    @permission_required('基金管理')
    @params_required(*['pool_type'])
    @check_pool_type_valid
    def get(self):
        fund_ids = FundPool.get_fund_ids(self.input.pool_type)
        return fund_ids

    @login_required
    @permission_required('基金管理')
    @params_required(*['fund_ids', 'pool_type'])
    @check_pool_type_valid
    def post(self):
        FundPool.add_fund_ids(self.input.fund_ids, self.input.pool_type)
        return 'success'

    @login_required
    @permission_required('基金管理')
    @params_required(*['fund_ids', 'pool_type'])
    @check_pool_type_valid
    def delete(self):
        FundPool.delete_fund_ids(self.input.fund_ids, self.input.pool_type)
        return 'success'

