
from flask import g

from bases.exceptions import ParamsError, VerifyError
from bases.viewhandler import ApiViewHandler
from extensions.robo import Robo
from models import FundManager
from utils.decorators import login_required, params_required, permission_required


class FundManagerAPI(ApiViewHandler):

    @login_required
    @params_required(*['manager_id'])
    def get(self):
        manager_info = Robo.get_fund_manager_info([self.input.manager_id], g.user.id)
        if len(manager_info) == 0:
            raise VerifyError('基金经理不存在!')

        return manager_info[0]

    @login_required
    @permission_required('基金管理')
    @params_required(*['manager_id'])
    def post(self):
        FundManager.add_manager_id(self.input.manager_id)
        return 'success'

    @login_required
    @permission_required('基金管理')
    @params_required(*['manager_id'])
    def delete(self):
        FundManager.delete_manager_id(self.input.manager_id)
        return 'success'


class FundManagersAPI(ApiViewHandler):

    @login_required
    @permission_required('基金管理')
    def get(self):
        manager_ids = FundManager.get_manager_ids()
        return manager_ids

    @login_required
    @permission_required('基金管理')
    @params_required(*['manager_ids'])
    def post(self):
        FundManager.add_manager_ids(self.input.manager_ids)
        return 'success'

    @login_required
    @permission_required('基金管理')
    @params_required(*['manager_ids'])
    def delete(self):
        FundManager.delete_manager_ids(self.input.manager_ids)
        return 'success'


class FundManagerInfosAPI(ApiViewHandler):

    @login_required
    def get(self):
        manager_ids = FundManager.get_manager_ids()
        manager_info = Robo.get_fund_manager_info(manager_ids, g.user.id)
        return manager_info

    @login_required
    @params_required(*['manager_ids'])
    def post(self):
        if not isinstance(self.input.manager_ids, list):
            raise ParamsError('参数类型错误! (manager_ids){}'.format(self.input.manager_ids))

        manager_info = Robo.get_fund_manager_info(self.input.manager_ids, g.user.id)
        return manager_info

