
from flask import request

from bases.viewhandler import ApiViewHandler
from models import SectorInfo
from utils.decorators import login_required, params_required, permission_required

from .libs.sectors import check_sector_name_valid, get_sector_info, get_sector_list_info


class SectorNameAPI(ApiViewHandler):

    @params_required(*['sector_name'])
    def get(self):
        sector_id = request.args.get('sector_id')
        check_sector_name_valid(sector_name=self.input.sector_name, sector_id=sector_id)
        return 'success'

    @params_required(*['tag_names'])
    def post(self):
        sector_id = request.json.get('sector_id')
        check_sector_name_valid(tag_names=self.input.tag_names, sector_id=sector_id)
        return 'success'


class SectorInfoAPI(ApiViewHandler):

    @login_required
    @permission_required('基金管理')
    @params_required(*['sector_id'])
    def get(self):
        '''获取板块'''
        return get_sector_info(self.input.sector_id)

    @login_required
    @permission_required('基金管理')
    @params_required(*['sector_name', 'tag_names', 'fund_ids'])
    def post(self):
        '''创建板块'''
        check_sector_name_valid(self.input.sector_name, self.input.tag_names)

        sector = SectorInfo.create_sector(
            self.input.sector_name, request.json.get('remark', ''), self.input.tag_names, self.input.fund_ids,
        )

        return {'sector_id': sector.id}

    @login_required
    @permission_required('基金管理')
    @params_required(*['sector_id', 'sector_name', 'tag_names', 'fund_ids'])
    def put(self):
        '''更新板块'''
        check_sector_name_valid(self.input.sector_name, self.input.tag_names, self.input.sector_id)

        SectorInfo.get_by_id(self.input.sector_id).update_sector(
            self.input.sector_name, request.json.get('remark', ''), self.input.tag_names, self.input.fund_ids,
        )

        return 'success'

    @login_required
    @permission_required('基金管理')
    @params_required(*['sector_id'])
    def delete(self):
        '''删除板块'''
        SectorInfo.get_by_id(self.input.sector_id).delete_sector()
        return 'success'


class SectorInfosAPI(ApiViewHandler):

    @login_required
    @permission_required('基金管理')
    def get(self):
        '''获取板块列表'''
        return get_sector_list_info()

