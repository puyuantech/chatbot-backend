import uuid
import datetime

from bases.constants import TOKEN_EXPIRATION_IN_MINUTES, TOKEN_MAX_NUM
from bases.dbwrapper import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    """
    用户
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(31))
    sex = db.Column(db.Integer, default=0, nullable=False)  # 1表示男，2表示女，其它未知
    email = db.Column(db.String(64), nullable=True)
    avatar_url = db.Column(db.String(128))
    site = db.Column(db.String(256))
    role_id = db.Column(db.Integer, default=0)  # role_id 是否是管理员或者其他权限 0是一般用户 1 管理员用户
    is_staff = db.Column(db.BOOLEAN, default=False)  # 是否是员工
    privacy_level = db.Column(db.Integer, default=0)  # 0 所有人可以查看我的回复 我的主题 1 只有登录的人可以查看 2 只有自己可以查看

    roles = db.relationship(
        'Role',
        secondary='map_user_role',
        backref='user',
     )

    def to_normal_dict(self):
        return {
            'id': self.id,
            'nick_name': self.nick_name,
            'sex': self.sex,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'site': self.site,
            'role_id': self.role_id,
            'is_staff': self.is_staff,
            'privacy_level': self.privacy_level,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

    @staticmethod
    def get_all_user_info(user_login):
        user_dict = user_login.to_dict(remove_fields_list=['password_hash'])
        user_login.last_login = datetime.datetime.now()
        user_login.save()
        user_info = User.get_by_id(user_login.user_id)
        user_dict.update(user_info.to_dict())
        return user_dict


class UserLogin(BaseModel):
    """
    用户登录表
    """
    __tablename__ = 'user_login'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    last_login = db.Column(db.DATETIME, default=datetime.datetime.now)

    @property
    def password(self):
        raise AttributeError("当前属性不可读")  # _password

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Token(BaseModel):
    """
    用户token
    """
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)      # 编号
    key = db.Column(db.String(32))                         # key值
    refresh_key = db.Column(db.String(32))                 # 刷新key值
    expires_at = db.Column(db.DateTime, nullable=False)  # 过期时间
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='token')

    @staticmethod
    def generate_key():
        return uuid.uuid4().hex

    @staticmethod
    def generate_expires_at():
        return datetime.datetime.now() + datetime.timedelta(minutes=TOKEN_EXPIRATION_IN_MINUTES)

    def is_valid(self):
        return datetime.datetime.now() < self.expires_at

    def refresh(self, refresh_key):
        if self.refresh_key == refresh_key:
            self.key = self.generate_key()
            self.expires_at = self.generate_expires_at()

    @classmethod
    def generate_token(cls, user_id):
        tokens = cls.filter_by_query(
            user_id=user_id,
        ).order_by(cls.expires_at.asc()).all()

        if len(tokens) < TOKEN_MAX_NUM:
            token = cls.create(
                key=cls.generate_key(),
                refresh_key=cls.generate_key(),
                expires_at=cls.generate_expires_at(),
                user_id=user_id,
            )
        else:
            token = tokens[0]
            token.refresh(token.refresh_key)
            token.save()

        token = cls.get_by_id(token.id)
        return token.to_dict()

