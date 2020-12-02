
from flask import g

from bases.viewhandler import ApiViewHandler
from utils.decorators import params_required, bot_login
from models import RiskAnswer, RiskQuestion, ChatbotUserInfo

from .libs import calc_risk_score
from .constants import get_risk_level_by_score, UserRiskLevel, UserRiskLevelExplanation


class EvaluationAPI(ApiViewHandler):

    @bot_login
    def get(self):
        return ChatbotUserInfo.get_by_id(g.user.id).to_dict()

    @bot_login
    @params_required(*['answer'])
    def post(self):
        score = calc_risk_score(self.input.answer)
        risk_level = get_risk_level_by_score(score)
        RiskAnswer.save_risk_answer(g.user.id, risk_level, self.input.answer, score, g.user)

        return {'risk_level': risk_level}


class EvalExplanation(ApiViewHandler):
    @bot_login
    def get(self):
        return {
            'explanation': UserRiskLevelExplanation.get_name_2_code(),
            'risk_level': UserRiskLevel.get_name_2_code(),
        }


class EvalQuestion(ApiViewHandler):
    @bot_login
    def get(self):
        return [i.to_normal_dict() for i in RiskQuestion.filter_by_query()]
