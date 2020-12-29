
from sqlalchemy import distinct

from bases.dbwrapper import db, BaseModel


class SectorInfo(BaseModel):
    '''板块信息'''
    __tablename__ = 'sectors'

    id = db.Column(db.Integer, primary_key=True)
    sector_name = db.Column(db.String(20))
    remark = db.Column(db.String(128))

    @classmethod
    def get_sector_names(cls, exclude_id=None):
        sector_names = db.session.query(cls.sector_name).filter_by(is_deleted=False)
        if exclude_id is not None:
            sector_names = sector_names.filter(cls.id != exclude_id)
        return set(sector_name for sector_name, in sector_names.all())

    @classmethod
    def create_sector(cls, sector_name, remark, tag_names, fund_ids):
        self = cls.create()

        try:
            self.update_sector(sector_name, remark, tag_names, fund_ids)
        except Exception as e:
            self.delete()
            raise e

        return self

    def update_sector(self, sector_name, remark, tag_names, fund_ids):
        self.update(
            commit=False,
            sector_name=sector_name,
            remark=remark,
        )

        SectorTag.update_sector_tags(self.id, tag_names, commit=False)
        SectorFund.update_sector_funds(self.id, fund_ids, commit=False)

        db.session.commit()

    def delete_sector(self):
        self.logic_delete(commit=False)

        for sector_tag in SectorTag.filter_by_query(sector_id=self.id).all():
            sector_tag.logic_delete(commit=False)

        for sector_fund in SectorFund.filter_by_query(sector_id=self.id).all():
            sector_fund.logic_delete(commit=False)

        db.session.commit()


class SectorTag(BaseModel):
    '''板块别名'''
    __tablename__ = 'sector_tags'

    id = db.Column(db.Integer, primary_key=True)
    sector_id = db.Column(db.Integer)
    tag_name = db.Column(db.String(20))

    @classmethod
    def get_tag_names(cls, exclude_id=None):
        tag_names = db.session.query(distinct(cls.tag_name)).filter_by(is_deleted=False)
        if exclude_id is not None:
            tag_names = tag_names.filter(cls.sector_id != exclude_id)
        return set(tag_name for tag_name, in tag_names.all())

    @classmethod
    def update_sector_tags(cls, sector_id, tag_names, commit=True):
        sector_tags = cls.filter_by_query(sector_id=sector_id).all()
        sector_tags = {sector_tag.tag_name: sector_tag for sector_tag in sector_tags}

        to_add_tags = set(tag_names) - set(sector_tags)
        to_del_tags = set(sector_tags) - set(tag_names)

        for tag_name in to_add_tags:
            cls(sector_id=sector_id, tag_name=tag_name).save(commit=commit)

        for tag_name in to_del_tags:
            sector_tags[tag_name].logic_delete(commit=commit)


class SectorFund(BaseModel):
    '''板块基金'''
    __tablename__ = 'sector_funds'

    id = db.Column(db.Integer, primary_key=True)
    sector_id = db.Column(db.Integer)
    fund_id = db.Column(db.String(20))

    @classmethod
    def update_sector_funds(cls, sector_id, fund_ids, commit=True):
        sector_funds = cls.filter_by_query(sector_id=sector_id).all()
        sector_funds = {sector_fund.fund_id: sector_fund for sector_fund in sector_funds}

        to_add_funds = set(fund_ids) - set(sector_funds)
        to_del_funds = set(sector_funds) - set(fund_ids)

        for fund_id in to_add_funds:
            cls(sector_id=sector_id, fund_id=fund_id).save(commit=commit)

        for fund_id in to_del_funds:
            sector_funds[fund_id].logic_delete(commit=commit)

