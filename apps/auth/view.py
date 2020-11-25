
from flask import g, request
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from extensions.wx.mini import *
from models import WeChatUnionID, Token
from utils.decorators import params_required, login_required
from apps.captchas.libs import check_img_captcha
from .libs import check_login, get_all_user_info, register_user


class LoginAPI(ApiViewHandler):
    @params_required(*['username', 'password', 'verification_code', 'verification_key'])
    def post(self):
        check_img_captcha(
            verification_code=self.input.verification_code,
            verification_key=self.input.verification_key,
        )
        user_login = check_login(
            username=self.input.username,
            password=self.input.password,
        )
        user_dict = get_all_user_info(user_login)
        token_dict = Token.generate_token(user_login.user_id)

        data = {
            'user': user_dict,
            'token': token_dict,
        }
        return data


class Logout(ApiViewHandler):

    @login_required
    def get(self):
        g.token.delete()

    def post(self):
        return self.get()


class RegisterAPI(ApiViewHandler):
    @params_required(*['username', 'password'])
    def post(self):
        if not self.is_valid_password(self.input.password):
            raise VerifyError('Password should contain both numbers and letters,'
                              ' and the length should be between 8-16 bits !')
        register_user(self.input.username, self.input.password)


class Logic(ApiViewHandler):

    def get(self):
        print(request.headers)
        print(request.data)
        print(request)


class WXMiniLogin(ApiViewHandler):

    @params_required(*['mini_type', 'code', 'iv', 'encrypted_data', 'user_info'])
    def get(self):
        user_info = self.input.user_info
        union_info = WXUnion.get_union_id(
            self.input.mini_type,
            self.input.code,
            self.input.iv,
            self.input.encrypted_data,
        )
        user_id = WeChatUnionID.get_user_id(union_info['unionid'])

        if not user_id:
            user = User.register_from_mini(
                nick_name=user_info.get('nickName'),
                head_img_url=user_info.get('avatarUrl'),
                union_id=union_info['unionid'],
                source=source,
                advisor_id=advisor_id,
            )
            user_id = user['user_id']

        else:
            user = User.login(user_id, brand_id)
            advisor_id = user_id if user['is_adviser'] else BrandAdvisor.get_advisor_id(user_id, brand_id)

        token = Token.generate_token(user_id)
        data = {'msg': '登录成功', 'advisor_id': advisor_id}
        data.update(user)
        data.update(token)

        return SUCCESS_RSP(data=data)

