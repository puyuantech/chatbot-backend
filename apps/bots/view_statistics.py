
from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from models import ChatbotDialogStat, ChatbotProductView, ChatbotUserInfo
from utils.decorators import login_required

from .libs.statistics import get_dialog_count, get_product_daily_view, get_user_count


class ExpertiseDistributionAPI(ApiViewHandler):

    @login_required
    def get(self):
        """查询用户专业度分布统计"""
        return ChatbotUserInfo.get_expertise_distribution()


class RiskToleranceDistributionAPI(ApiViewHandler):

    @login_required
    def get(self):
        """查询用户风险承受能力分布统计"""
        return ChatbotUserInfo.get_risk_tolerance_distribution()


class DialogCountDistributionAPI(ApiViewHandler):

    @login_required
    def get(self):
        """查询用户对话量分布统计"""
        return ChatbotDialogStat.get_dialog_count_distribution()


class ProductViewCountAPI(ApiViewHandler):

    @login_required
    def get(self):
        """获取产品浏览量排行"""
        top_n = self.input.top_n
        if top_n:
            top_n = int(top_n)
            if top_n <= 0:
                raise VerifyError('top_n参数不合法！')

        return ChatbotProductView.get_product_view_count(
            self.input.user_id, self.input.wechat_group_id, self.input.start_time, self.input.end_time, top_n
        )


class UserCountAPI(ApiViewHandler):

    @login_required
    def get(self):
        """查询用户量统计（总量+日活）"""
        return get_user_count(self.input.start_time, self.input.end_time)


class DialogCountAPI(ApiViewHandler):

    @login_required
    def get(self):
        """查询对话量统计"""
        return get_dialog_count(self.input.user_id, self.input.start_time, self.input.end_time)


class ProductDailyViewAPI(ApiViewHandler):

    @login_required
    def get(self):
        """查询产品每日浏览量统计"""
        return get_product_daily_view(self.input.user_id, self.input.start_time, self.input.end_time)

