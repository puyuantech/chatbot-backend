
from bases.dbwrapper import db, BaseModel
from bases.exceptions import VerifyError


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
    def add_fund_ids(cls, fund_ids, pool_type, silent=True):
        existing_fund_ids = cls.get_fund_ids(pool_type)
        for fund_id in fund_ids:
            if fund_id in existing_fund_ids:
                if not silent:
                    raise VerifyError('基金已存在!')
                continue
            cls(fund_id=fund_id, pool_type=pool_type).save(commit=False)
        db.session.commit()

    @classmethod
    def delete_fund_ids(cls, fund_ids, pool_type, silent=True):
        funds = cls.query.filter(
            cls.pool_type == pool_type,
            cls.is_deleted == False,
            cls.fund_id.in_(fund_ids),
        ).all()

        if not silent and len(set(fund_ids)) > len(funds):
            raise VerifyError('基金不存在!')

        for fund in funds:
            fund.logic_delete(commit=False)
        db.session.commit()

    @classmethod
    def add_fund_id(cls, fund_id, pool_type):
        cls.add_fund_ids([fund_id], pool_type, silent=False)

    @classmethod
    def delete_fund_id(cls, fund_id, pool_type):
        cls.delete_fund_ids([fund_id], pool_type, silent=False)


class FundManager(BaseModel):
    '''明星基金经理'''
    __tablename__ = 'fund_managers'

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.CHAR(20))

    @classmethod
    def get_manager_ids(cls):
        managers = cls.filter_by_query().all()
        return [manager.manager_id for manager in managers]

    @classmethod
    def add_manager_ids(cls, manager_ids, silent=True):
        existing_manager_ids = cls.get_manager_ids()
        for manager_id in manager_ids:
            if manager_id in existing_manager_ids:
                if not silent:
                    raise VerifyError('基金经理已存在!')
                continue
            cls(manager_id=manager_id).save(commit=False)
        db.session.commit()

    @classmethod
    def delete_manager_ids(cls, manager_ids, silent=True):
        managers = cls.query.filter(
            cls.is_deleted == False,
            cls.manager_id.in_(manager_ids),
        ).all()

        if not silent and len(set(manager_ids)) > len(managers):
            raise VerifyError('基金经理不存在!')

        for manager in managers:
            manager.logic_delete(commit=False)
        db.session.commit()

    @classmethod
    def add_manager_id(cls, manager_id):
        cls.add_manager_ids([manager_id], silent=False)

    @classmethod
    def delete_manager_id(cls, manager_id):
        cls.delete_manager_ids([manager_id], silent=False)

