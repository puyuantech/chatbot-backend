from bases.dbwrapper import BaseModel, db
from utils.helper import json_str_to_dict
from .chat_bot import ChatbotUserInfo


class RiskQuestion(BaseModel):
    """风险测评列表"""
    __tablename__ = "eval_questions"

    id = db.Column(db.Integer, primary_key=True)          # 编号
    order_num = db.Column(db.Integer)                     # 序号
    question = db.Column(db.VARCHAR(255))                 # 问题
    symbol = db.Column(db.VARCHAR(32))                    # 答案选项  ['A', 'B', ...] 与answer对应
    answer = db.Column(db.Text)                           # 答案    ['answer1', 'answer2', ...]
    score = db.Column(db.VARCHAR(64))                     # 得分

    def to_normal_dict(self):
        return {
            'id': self.id,
            'order_num': self.order_num,
            'question': self.question,
            'symbol': json_str_to_dict(self.symbol),
            'answer': json_str_to_dict(self.answer),
            'score': json_str_to_dict(self.score),
        }


class RiskAnswer(BaseModel):
    """风险测评结果"""
    __tablename__ = "eval_answers"

    id = db.Column(db.Integer, primary_key=True)              # 编号
    user_id = db.Column(db.Integer)                           # 用户id
    answer = db.Column(db.VARCHAR(63))                        # 答案    'A,B,C'
    score = db.Column(db.Integer)                             # 得分
    risk_level = db.Column(db.CHAR(2), default='')            # 风险等级

    @classmethod
    def get_risk_answer(cls, user_id) -> dict:
        risk = cls.filter_by_query(user_id=user_id).one_or_none()
        return risk and risk.to_dict() or {}

    @classmethod
    def save_risk_answer(cls, user_id, risk_level, answer, score, user):
        old = cls.filter_by_query(user_id=user_id).one_or_none()
        if old:
            old.delete()

        new = cls(
            user_id=user_id,
            answer=answer,
            score=score,
            risk_level=risk_level,
        )

        user.risk_tolerance = score / 50
        db.session.add(new)
        db.session.commit()

