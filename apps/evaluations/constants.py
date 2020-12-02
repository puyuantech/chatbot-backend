from bases.base_enmu import EnumBase


class UserRiskLevel(EnumBase):
    安逸型 = '01'
    保守型 = '02'
    稳健型 = '03'
    积极型 = '04'
    进取型 = '05'


class UserRiskLevelExplanation(EnumBase):
    安逸型 = '风险承受能力极低，追求本金的绝对安全，只能购买低风险承受能力的产品。'
    保守型 = '风险承受度低，资产配置以低风险为主，为了获取收益能容忍极少的本金损失，止损意识强。'
    稳健型 = '风险承受能力适中，偏向于均衡的资产配置，为了获取收益能够承受一定的投资风险。'
    积极型 = '风险承受能力强，偏向于激进的资产配置，投资收益预期相对较高，为了获取预期收益可以承受资产市值的较大波动。'
    进取型 = '风险承受能力非常强，投机性强，追求收益最大化，为了获取预期收益可以承受资产市值的超大幅波动。'


def get_risk_level_by_score(score):
    if score <= 19:
        return UserRiskLevel.安逸型
    if score <= 26:
        return UserRiskLevel.保守型
    if score <= 34:
        return UserRiskLevel.稳健型
    if score <= 42:
        return UserRiskLevel.积极型
    return UserRiskLevel.进取型
