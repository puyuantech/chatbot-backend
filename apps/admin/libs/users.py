from .staff import get_user_by_username
from bases.exceptions import VerifyError
from models import UserLogin, User


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
    return user, user_login

