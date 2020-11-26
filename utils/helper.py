import jwt
import datetime


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedPrint:
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            endpoint = options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)


class ShareTokenAuth:

    @staticmethod
    def encode(payload, secret_key):
        """
        生成认证Token
        :param payload: dict
        :param secret_key:
        :return: string
        """
        return jwt.encode(
            payload,
            secret_key,
        )

    @staticmethod
    def decode(token, secret_key):
        """
        验证Token
        :param token:
        :param secret_key
        :return: integer|string
        """
        try:
            payload = jwt.decode(token, secret_key, leeway=datetime.timedelta(minutes=1))
            # 取消过期时间验证
            # payload = jwt.decode(auth_token, secret_key, options={'verify_exp': False})
            # 参数对验证
            if 'data' in payload:
                return True, payload
            raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return False, 'Token过期'
        except jwt.InvalidTokenError:
            return False, '无效Token'


def _RESPONSE(data, msg, code, status_code):
    from flask import jsonify
    rsp = {
        'code': code,
        'data': data,
        'msg': msg,
    }

    return jsonify(rsp), status_code


def SUCCESS_RSP(data="success", msg=None):
    return _RESPONSE(data, msg, 1000, 200)


def ACCEPTED_RSP(data="success", msg=None):
    return _RESPONSE(data, msg, 1000, 202)


def ERROR_RSP(data=None, msg=None, code=None, status_code=400):
    return _RESPONSE(data, msg, code, status_code)


def generate_sql_pagination():
    from flask import request
    from bases.paginations import SQLPagination
    page = request.args.get('page', 1)
    page_size = request.args.get('page_size', 10)
    ordering = request.args.get('ordering')
    if ordering:
        ordering = ordering.split(',')

    return SQLPagination(page, page_size, ordering)


if __name__ == '__main__':
    code = ShareTokenAuth.encode(
        {'data': {'name': 1}},
        '1'
    )
    print(code)
    print(ShareTokenAuth.decode(code, '1'))


