
from flask import request

from bases.globals import db
from bases.viewhandler import ApiViewHandler
from models import SectorFund, SectorInfo, SectorTag
from utils.decorators import login_required, params_required, permission_required

from .libs.sectors import check_sector_name_valid, get_sector_info


class SectorNameAPI(ApiViewHandler):

    @params_required(*['sector_name', 'tag_names'])
    def post(self):
        sector_id = request.json.get('sector_id')
        check_sector_name_valid(self.input.sector_name, self.input.tag_names, sector_id)
        return 'success'


class SectorInfoAPI(ApiViewHandler):

    @login_required
    @permission_required('基金管理')
    @params_required(*['sector_id'])
    def get(self):
        '''获取板块信息'''
        return get_sector_info(self.input.sector_id)

    @login_required
    @permission_required('基金管理')
    @params_required(*['sector_name', 'tag_names', 'remark', 'fund_ids'])
    def post(self):
        '''创建板块'''
        check_sector_name_valid(self.input.sector_name, self.input.tag_names)

        sector = SectorInfo.create(
            sector_name=self.input.sector_name,
            remark=self.input.remark,
        )
        try:
            SectorTag.update_sector_tags(sector.id, self.input.tag_names, commit=False)
            SectorFund.update_sector_funds(sector.id, self.input.fund_ids, commit=False)

            db.session.commit()
        except Exception as e:
            sector.delete()
            raise e

        return sector.id

    @login_required
    @permission_required('基金管理')
    @params_required(*['sector_id', 'sector_name', 'tag_names', 'remark', 'fund_ids'])
    def put(self):
        '''更新板块'''
        check_sector_name_valid(self.input.sector_name, self.input.tag_names, self.input.sector_id)

        SectorInfo.get_by_id(self.input.sector_id).update(
            commit=False,
            sector_name=self.input.sector_name,
            remark=self.input.remark,
        )

        SectorTag.update_sector_tags(self.input.sector_id, self.input.tag_names, commit=False)
        SectorFund.update_sector_funds(self.input.sector_id, self.input.fund_ids, commit=False)

        db.session.commit()
        return 'success'

    @login_required
    @permission_required('基金管理')
    @params_required(*['sector_id'])
    def delete(self):
        '''删除板块'''
        SectorInfo.get_by_id(self.input.sector_id).logic_delete(commit=False)

        for sector_tag in SectorTag.filter_by_query(sector_id=self.input.sector_id).all():
            sector_tag.logic_delete(commit=False)

        for sector_fund in SectorFund.filter_by_query(sector_id=self.input.sector_id).all():
            sector_fund.logic_delete(commit=False)

        db.session.commit()
        return 'success'

