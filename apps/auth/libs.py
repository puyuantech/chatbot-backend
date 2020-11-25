import datetime
from models import User, UserLogin, Token
from bases.exceptions import AuthError, VerifyError


def get_user_by_username(username):
    return UserLogin.filter_by_query(username=username).first()


def check_login(username, password):
    user_login = get_user_by_username(username)
    if not user_login:
        raise AuthError("用户名不存在")
    if not user_login.check_password(password):
        raise AuthError("密码错误")
    if user_login.is_deleted:
        raise AuthError("账户已经停用")
    return user_login


def get_all_user_info(user_login):
    user_dict = user_login.to_dict(remove_fields_list=['password_hash'])
    user_login.last_login = datetime.datetime.now()
    user_login.save()
    user_info = User.get_by_id(user_login.user_id)
    user_dict.update(user_info.to_dict())
    return user_dict


def register_user(username, password):
    if get_user_by_username(username):
        raise VerifyError('用户名已存在！')
    user = User.create(
        nick_name=username,
    )
    try:
        user_login = UserLogin.create(
            user_id=user.id,
            username=username,
            password=password,
        )
    except Exception as e:
        user.delete()
        raise e
    return user_login


def register_from_mini():
    pass


