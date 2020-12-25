
from bases.dbwrapper import db, BaseModel


class FundPool(BaseModel):
    '''基金池'''
    __tablename__ = 'fund_pools'

    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.CHAR(20))
    pool_type = db.Column(db.CHAR(10))  # 基金池类型: basic, new, old

    @classmethod
    def get_fund_ids(cls, pool_type):
        funds = cls.filter_by_query(pool_type=pool_type).all()
        return [fund.fund_id for fund in funds]

    @classmethod
    def delete_fund_ids(cls, fund_ids, pool_type):
        if not fund_ids:
            return

        funds = cls.query.filter(
            cls.pool_type == pool_type,
            cls.is_deleted == False,
            cls.fund_id.in_(fund_ids),
        ).all()

        for fund in funds:
            fund.logic_delete(commit=False)

        db.session.commit()

