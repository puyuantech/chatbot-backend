
from flask import g

from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from extensions.robo import Robo
from models import FundPool, SectorInfo
from utils.decorators import login_required, params_required, permission_required

from .constants import RecommendFundType
from .libs.recommend import get_match_risk_level


class FundRecommendMenuAPI(ApiViewHandler):

    @login_required
    @permission_required('推荐基金')
    def get(self):
        return {
            '行业板块': [sector.sector_name for sector in SectorInfo.filter_by_query().all()],
            '能力维度': ['收益能力', '抗风险能力', '稳定性', '择时能力', '选股能力', '管理能力'],
            '投资偏好': ['打新', '可转债', '绝对收益'],
            '主要指数': list(Robo.get_index_list().keys()),
            '基金类型': sorted(RecommendFundType.get_codes()),
            'ETF基金': ['场外', '场内'],
            '明星基金': ['新星', '老司机'],
        }


class FundRecommendBySectorAPI(ApiViewHandler):

    @login_required
    @params_required(*['sector_name'])
    @get_match_risk_level
    def post(self):
        fund_ids = SectorInfo.get_funds_by_sector_name(self.input.sector_name)
        fund_info = Robo.get_fund_by_recommend(fund_ids, g.user.id, self.input.risk_level)
        return fund_info


class FundRecommendByAbilityAPI(ApiViewHandler):

    @login_required
    @params_required(*['ability'])
    @get_match_risk_level
    def post(self):
        fund_ids = FundPool.get_fund_ids('basic')

        if self.input.ability in ('业绩', '收益', '收益能力'):
            ordering = '-收益能力'
        elif self.input.ability in ('风险', '抗风险能力'):
            ordering = '-抗风险能力'
        elif self.input.ability in ('稳定', '稳定性'):
            ordering = '-稳定能力'
        elif self.input.ability in ('择时', '择时能力'):
            ordering = '-择时能力'
        elif self.input.ability in ('选股', '选股能力'):
            ordering = '-选股能力'
        elif self.input.ability in ('管理能力', '团队', '基金经理'):
            ordering = '-基金经理评分'
        else:
            ordering = None

        fund_info = Robo.get_fund_by_recommend(fund_ids, g.user.id, self.input.risk_level, ordering=ordering)
        return fund_info


class FundRecommendByFundTypeAPI(ApiViewHandler):

    @login_required
    @params_required(*['fund_type'])
    @get_match_risk_level
    def post(self):
        fund_ids = FundPool.get_fund_ids('basic')
        fund_info = Robo.get_fund_by_recommend(fund_ids, g.user.id, self.input.risk_level, filters={'基金类型': self.input.fund_type})
        return fund_info


class FundRecommendByPreferenceAPI(ApiViewHandler):

    @login_required
    @params_required(*['preference'])
    @get_match_risk_level
    def post(self):
        fund_ids = FundPool.get_fund_ids('basic')

        if self.input.preference == '打新':
            filters = {'是否是打新基金': 1}
        elif self.input.preference == '可转债':
            filters = {'是否是可转债基金': 1}
        elif self.input.preference == '绝对收益':
            filters = {'是否是绝对收益基金': 1}
        else:
            filters = None

        fund_info = Robo.get_fund_by_recommend(fund_ids, g.user.id, self.input.risk_level, filters=filters)
        return fund_info


class FundRecommendByIndexAPI(ApiViewHandler):

    @login_required
    @params_required(*['index'])
    @get_match_risk_level
    def post(self):
        index_list = Robo.get_index_list()
        if self.input.index not in index_list:
            raise VerifyError('精选指数不存在! (index){}'.format(self.input.index))

        fund_ids = FundPool.get_fund_ids('basic')
        index_code = index_list[self.input.index]
        contains = {'指数列表': f'"{index_code}"'}

        fund_info = Robo.get_fund_by_recommend(fund_ids, g.user.id, self.input.risk_level, contains=contains)
        return fund_info


class FundRecommendByXirrAPI(ApiViewHandler):

    @login_required
    @params_required(*['init_bench', 'amt_bench', 'tot_mv', 'periods', 'risk_level'])
    def post(self):
        fund_ids = FundPool.get_fund_ids('basic')
        fund_info = Robo.get_fund_by_recommend_xirr(
            fund_ids, g.user.id, self.input.risk_level, self.input.init_bench,
            self.input.amt_bench, self.input.tot_mv, self.input.periods,
        )
        return fund_info


class FundRecommendByRiskIncomeAPI(ApiViewHandler):

    @login_required
    @params_required(*['min_income', 'max_income', 'min_risk', 'max_risk', 'risk_level'])
    def post(self):
        fund_ids = FundPool.get_fund_ids('basic')
        fund_info = Robo.get_fund_by_recommend_risk_income(
            fund_ids, g.user.id, self.input.risk_level, self.input.min_income / 100,
            self.input.max_income / 100, self.input.min_risk / 100, self.input.max_risk / 100,
        )
        return fund_info


class FundRecommendByBenchmarkAPI(ApiViewHandler):

    @login_required
    @params_required(*['benchmark', 'comparison', 'digital'])
    def post(self):
        fund_ids = FundPool.get_fund_ids('basic')

        min_income = max_income = min_risk = max_risk = None
        digital = self.input.digital / 100
        if self.input.benchmark == '年化收益':
            if self.input.comparison in ('大于', '超过', '达到', '不小于', '高于'):
                min_income = digital
            else:
                max_income = digital
        else:
            if self.input.comparison in ('大于', '超过', '达到', '不小于', '高于'):
                min_risk = digital
            else:
                max_risk = digital

        fund_info = Robo.get_fund_by_recommend_risk_income(
            fund_ids, g.user.id, None, min_income, max_income, min_risk, max_risk,
        )
        return fund_info


class FundRecommendByHoldStockAPI(ApiViewHandler):

    @login_required
    @params_required(*['stock_name'])
    def post(self):
        fund_ids = FundPool.get_fund_ids('basic')
        fund_info = Robo.get_fund_by_recommend_hold_stock(fund_ids, g.user.id, self.input.stock_name)
        return fund_info


class FundRecommendByHoldBondAPI(ApiViewHandler):

    @login_required
    @params_required(*['bond_name'])
    def post(self):
        fund_ids = FundPool.get_fund_ids('basic')
        fund_info = Robo.get_fund_by_recommend_hold_bond(fund_ids, g.user.id, self.input.bond_name)
        return fund_info


class FundRecommendByETFAPI(ApiViewHandler):

    @login_required
    @params_required(*['index', 'etf_type'])
    def post(self):
        fund_info = Robo.get_fund_by_recommend_etf(g.user.id, self.input.index, self.input.etf_type)
        return fund_info


class FundRecommendByKeyAPI(ApiViewHandler):

    @login_required
    @params_required(*['ordering'])
    def post(self):
        fund_info = Robo.get_fund_by_recommend(None, g.user.id, None, ordering=self.input.ordering)
        return fund_info

