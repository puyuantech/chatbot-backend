
from bases.viewhandler import ApiViewHandler
from extensions.robo import Robo
from models import SectorInfo
from utils.decorators import login_required, permission_required

from .constants import RecommendFundType


class FundRecommendMenuAPI(ApiViewHandler):

    @login_required
    @permission_required('推荐基金')
    def get(self):
        return {
            '行业板块': [sector.sector_name for sector in SectorInfo.filter_by_query().all()],
            '能力维度': ['收益能力', '抗风险能力', '稳定性', '择时能力', '选股能力', '管理能力'],
            '投资偏好': ['打新', '可转债', '绝对收益'],
            '主要指数': Robo.get_index_list(),
            '基金类型': sorted(RecommendFundType.get_codes()),
            'ETF基金': ['场外', '场内'],
            '明星基金': ['新星', '老司机'],
        }

