
import functools

from flask import g, request

from bases.exceptions import AuthError, AuthPermissionError, LogicError
from models import UserLogin


def login_required(func):
    @functools.wraps(func)
    def _func_wrapper(cls, *args, **kwargs):
        from apps.auth.authtoken import TokenAuthentication
        user, token = TokenAuthentication().authenticate(request)
        if not user:
            raise AuthError('请先登录')
        user_login = UserLogin.filter_by_query(user_id=user.id).first()
        g.user = user
        g.user_login = user_login
        g.token = token

        return func(cls, *args, **kwargs)
    return _func_wrapper


def view_login_required(func):
    @functools.wraps(func)
    def _func_wrapper(*args, **kwargs):
        from apps.auth.authtoken import TokenAuthentication
        user, token = TokenAuthentication().authenticate(request)
        if not user:
            raise AuthError('请先登录')
        user_login = UserLogin.filter_by_query(user_id=user.id).first()
        g.user = user
        g.user_login = user_login
        g.token = token

        return func(*args, **kwargs)
    return _func_wrapper


def bot_login(func):
    @functools.wraps(func)
    def _func_wrapper(cls, *args, **kwargs):
        from apps.auth.authtoken import ChatTokenAuthentication
        user, token = ChatTokenAuthentication().authenticate(request)
        if not user:
            raise AuthError('请先登录')
        g.user = user
        g.token = token

        return func(cls, *args, **kwargs)
    return _func_wrapper


def super_admin_login_required(func):
    @functools.wraps(func)
    def _func_wrapper(cls, *args, **kwargs):
        from apps.auth.authtoken import TokenAuthentication
        user, token = TokenAuthentication().authenticate(request)
        if not user:
            raise AuthError('请先登录')
        if user.role_id != 1:
            raise AuthPermissionError('非超级管理员')
        user_login = UserLogin.filter_by_query(user_id=user.id).first()
        g.user = user
        g.user_login = user_login
        g.token = token

        return func(cls, *args, **kwargs)
    return _func_wrapper


def params_required(*params, **type_params):
    def dec(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            for arg in params:
                if getattr(self.input, arg) is None:
                    raise LogicError('需要:%s 参数' % arg)
                if getattr(self.input, arg) == '':
                    raise LogicError('参数:%s 不能为空' % arg)
            for k, _type in type_params.items():
                if getattr(self.input, k) is None:
                    raise LogicError('需要:%s 参数' % k)
                if getattr(self.input, k) == '':
                    raise LogicError('参数:%s 不能为空' % k)
                if not isinstance(getattr(self.input, k), _type):
                    raise LogicError('参数 "%s" 类型应该是: %s' % (k, _type))

            return func(self, *args, **kwargs)
        return wrapper
    return dec


def permission_required(permission_name):
    """必须在登录验证后使用此装饰器"""
    def dec(func):
        @functools.wraps(func)
        def _func_wrapper(cls, *args, **kwargs):
            if g.user.role_id != 1:
                permissions = {}
                for i in g.user.roles:
                    for j in i.permissions:
                        permissions[j.id] = j
                permissions = set([permissions[i].menu for i in permissions])
                if permission_name not in permissions:
                    raise AuthPermissionError('无权限访问')
            return func(cls, *args, **kwargs)
        return _func_wrapper

    return dec
