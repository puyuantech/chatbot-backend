from bases.globals import db
from bases.exceptions import LogicError
from models import RiskQuestion


def calc_risk_score(answer):
    questions = db.session.query(RiskQuestion).filter_by().order_by(
        RiskQuestion.order_num.asc()
    ).all()
    if not questions:
        raise LogicError('数据库问题不足！')
    questions = [i.to_normal_dict() for i in questions]

    rules = []
    for i in questions:
        r = {}
        score = i.get('score')
        for j, k in enumerate(i.get('symbol')):
            r[k] = score[j]
        rules.append(r)

    s = 0
    for i, j in enumerate(answer.split(',')):
        s += rules[i].get(j)

    return s


