from bases.globals import db
from bases.basehandler import BaseHandler
from bases.exceptions import BaseError
from flask import current_app
import copy
import datetime


def commit_session(*args):
    for i in args:
        db.session.add(i)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


class DBMixin(BaseHandler):
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance = instance.save()
        return instance

    @classmethod
    def create_by_uid(cls, **kwargs):
        instance = cls(**kwargs)
        instance.uid = cls.generate_hash_uuid(12)
        return instance

    @classmethod
    def get_by_id(cls, _id, show_deleted=False):
        query = db.session.query(cls).filter_by(id=_id)
        if not show_deleted:
            query = query.filter_by(is_deleted=False)
        instance = query.first()
        if not instance:
            raise BaseError(cls.__name__ + ' Not Find')
        return instance

    @classmethod
    def user_get_by_id(cls, _id, user_id):
        instance = db.session.query(cls).filter_by(id=_id, user_id=user_id, is_deleted=False).first()
        if not instance:
            raise BaseError(cls.__name__ + ' Not Find')
        return instance

    @classmethod
    def get_by_user(cls, user_id):
        instance = db.session.query(cls).filter_by(user_id=user_id, is_deleted=False).all()
        return instance

    @classmethod
    def get_by_uid(cls, uid):
        instance = db.session.query(cls).filter_by(uid=uid, is_deleted=False).first()
        if not instance:
            raise BaseError(cls.__name__ + ' Not Find')
        return instance

    @classmethod
    def get_by_query(cls, show_deleted=False, **query_dict):
        if show_deleted is False:
            query_dict['is_deleted'] = False
        instance = db.session.query(cls).filter_by(**query_dict).first()
        if not instance:
            raise BaseError(cls.__name__ + ' Not Find')
        return instance

    @classmethod
    def filter_by_query(cls, show_deleted=False, **query_dict):
        if query_dict.get('is_deleted'):
            query_dict.pop('is_deleted')

        if show_deleted is False:
            query_dict['is_deleted'] = False

        tmp = copy.deepcopy(query_dict)
        for k in tmp:
            if k not in cls.__dict__:
                query_dict.pop(k)
        return db.session.query(cls).filter_by(**query_dict)

    @classmethod
    def create_from_dict(cls, d):
        assert isinstance(d, dict)
        instance = cls(**d)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in list(kwargs.items()):
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                current_app.logger.error(e)
                db.session.rollback()
                raise e
        return self

    @classmethod
    def transaction_save(cls, *args):
        for i in args:
            db.session.add(i)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            raise e

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        return self

    def logic_delete(self, commit=True):
        self.is_deleted = True
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        return self

    def to_dict(self, fields_list=None, remove_fields_list=None, remove_deleted=True):
        if remove_fields_list:
            column_list = [column for column in self.__dict__ if column not in remove_fields_list]
        elif fields_list:
            column_list = [column for column in self.__dict__ if column in fields_list]
        else:
            column_list = self.__dict__

        data = copy.deepcopy({column_name: getattr(self, column_name)
                              for column_name in column_list})

        if data.get('_sa_instance_state'):
            data.pop('_sa_instance_state')

        if remove_deleted and data.get('is_deleted') is not None:
            data.pop('is_deleted')

        for k, v in data.items():
            if isinstance(v, datetime.datetime):
                data[k] = v.strftime('%Y-%m-%d %H:%M:%S')

        return data

    @classmethod
    def create_or_update(cls, query_dict, update_dict=None):
        instance = db.session.query(cls).filter_by(**query_dict).first()
        if instance:
            if update_dict is not None:
                return instance.update(**update_dict)
            else:
                return instance
        else:
            query_dict.update(update_dict or {})
            return cls.create(**query_dict)


class BaseModel(DBMixin, db.Model):
    """
    BaseModel
    """
    __abstract__ = True

    create_time = db.Column(db.DATETIME, default=datetime.datetime.now)
    update_time = db.Column(db.DATETIME, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 变更时间
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)  # 是否删除,默认不删除

