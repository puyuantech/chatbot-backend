
from collections import defaultdict
from flask import g

from bases.exceptions import VerifyError
from extensions.robo import Robo
from models import SectorFund, SectorInfo, SectorTag


def check_sector_name_valid(sector_name=None, tag_names=None, sector_id=None):
    sector_names = SectorInfo.get_sector_names(sector_id)

    if sector_name is not None:
        if tag_names is not None and sector_name in tag_names:
            raise VerifyError(f'板块名【{sector_name}】不能与别名重复!')

        if sector_name in sector_names:
            raise VerifyError(f'板块名【{sector_name}】已存在!')

        if sector_name in SectorTag.get_tag_names(sector_id):
            raise VerifyError(f'别名【{sector_name}】已存在, 板块名不能与别名重复!')

    if tag_names is not None:
        for tag_name in tag_names:
            if tag_name in sector_names:
                raise VerifyError(f'板块名【{tag_name}】已存在, 别名不能与板块名重复!')


def get_sector_info(sector_id):
    sector = SectorInfo.get_by_id(sector_id)

    sector_tags = SectorTag.filter_by_query(sector_id=sector_id).all()
    tag_names = [sector_tag.tag_name for sector_tag in sector_tags]

    sector_funds = SectorFund.filter_by_query(sector_id=sector_id).all()
    fund_ids = [sector_fund.fund_id for sector_fund in sector_funds]
    fund_info = Robo.get_fund_info(fund_ids, g.user.id)

    return {
        'sector_id': sector.id,
        'sector_name': sector.sector_name,
        'remark': sector.remark,
        'tag_names': tag_names,
        'fund_info': fund_info,
    }


def get_sector_list_info():
    sectors = SectorInfo.filter_by_query().all()

    sector_tags = defaultdict(list)
    for sector_tag in SectorTag.filter_by_query().all():
        sector_tags[sector_tag.sector_id].append(sector_tag.tag_name)

    sector_funds = defaultdict(list)
    for sector_fund in SectorFund.filter_by_query().all():
        sector_funds[sector_fund.sector_id].append(sector_fund.fund_id)

    return [
        {
            'sector_id': sector.id,
            'sector_name': sector.sector_name,
            'remark': sector.remark,
            'tag_names': sector_tags[sector.id],
            'fund_types': Robo.get_fund_types(sector_funds[sector.id]),
        }
        for sector in sectors
    ]

