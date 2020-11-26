import datetime
import time
import uuid
import ujson
import hashlib
import base64
import re


class BaseHandler(object):

    @classmethod
    def generate_hash_uuid(cls, limit=None):
        u = uuid.uuid4().hex
        if limit:
            u = u[:limit]
        return u

    @classmethod
    def get_datetime_now(cls):
        return datetime.datetime.now()

    @classmethod
    def get_timestamp(cls):
        return time.time()

    @classmethod
    def time_create(cls, t):
        return t.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def strptime(cls, t, f='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.strptime(t, f)

    @classmethod
    def get_datetime_utcnow(cls):
        return datetime.datetime.utcnow()

    @classmethod
    def from_timestamp(cls, timestamp):
        return datetime.datetime.fromtimestamp(timestamp)

    @classmethod
    def to_timestamp(cls, t):
        return time.mktime(t.timetuple())

    @classmethod
    def sha1(cls, string):
        return hashlib.sha1(string.encode('UTF-8') if isinstance(string, str) else string).hexdigest()

    @classmethod
    def b64encode(cls, bytestring):
        return base64.b64encode(bytestring.encode('UTF-8') if isinstance(bytestring, str) else bytestring)

    @classmethod
    def b64decode(cls, bytestring):
        return base64.b64decode(bytestring.encode('UTF-8') if isinstance(bytestring, str) else bytestring)

    @classmethod
    def dumps(cls, obj, ensure_ascii=False):
        return ujson.dumps(obj, ensure_ascii=ensure_ascii)

    @classmethod
    def loads(cls, string, default=None):
        return ujson.loads(string) if string else default

    @classmethod
    def timedelta(cls, **kwargs):
        return datetime.timedelta(**kwargs)

    @classmethod
    def is_valid_name(cls, name_str):
        pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]*$')
        return pattern.match(name_str)

    @classmethod
    def is_valid_email(cls, email_str):
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return pattern.match(email_str)

    @classmethod
    def is_valid_mobile(cls, mobile_str):
        pattern = re.compile(r"^1[345678][0-9]{9}$")
        return pattern.match(mobile_str)

    @classmethod
    def is_valid_password(cls, password_str):
        pattern = re.compile(r"^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$")
        return pattern.match(password_str)


class Dict(dict):
    def __getattr__(self, item):
        resp = self.get(item, None)
        if isinstance(resp, dict):
            resp = Dict(resp)
        return resp

    def __setattr__(self, key, value):
        self[key] = value
