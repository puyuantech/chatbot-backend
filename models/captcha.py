import datetime
from bases.dbwrapper import db, BaseModel
from bases.constants import IMG_CAPTCHA_EXPIRATION_IN_MINUTES


class CaptchaCode(BaseModel):
    __tablename__ = 'captcha_img'

    id = db.Column(db.Integer, primary_key=True)         # 编号
    key = db.Column(db.CHAR(64), default='')             # 缓存键
    value = db.Column(db.CHAR(64), default='')           # 验证码
    expires_at = db.Column(db.DATETIME, nullable=False)  # 过期时间

    @classmethod
    def generate_expires_at(cls):
        return datetime.datetime.now() + datetime.timedelta(minutes=IMG_CAPTCHA_EXPIRATION_IN_MINUTES)

    def is_valid(self, code):
        return self.value.lower() == code.lower() and datetime.datetime.now() < self.expires_at

