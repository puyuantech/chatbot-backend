
from bases.viewhandler import ApiViewHandler
from models import FundManager
from utils.decorators import login_required, params_required, permission_required


class FundManagerAPI(ApiViewHandler):

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

