import datetime
from flask import g, request, current_app
from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError, LogicError
from extensions.wx.mini import *
from models import WeChatUnionID, Token, ChatbotUserInfo, ChatBotToken
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
        current_app.logger.info(request.headers)
        print(request.headers)
        print(request.data)
        print(request)


class WXMiniLogin(ApiViewHandler):

    @params_required(*['app_name', 'code', 'iv', 'encrypted_data', 'user_info'])
    def post(self):
        user_info = self.input.user_info
        union_info = WXUnion.get_union_id(
            self.input.app_name,
            self.input.code,
            self.input.iv,
            self.input.encrypted_data,
        )
        user_id = WeChatUnionID.get_user_id(union_info['unionid'])

        if not user_id:
            user = ChatbotUserInfo.create(
                nick_name=user_info.get('nickName'),
                head_img=user_info.get('avatarUrl'),
                last_action_ts=datetime.datetime.now(),
            )
            try:
                WeChatUnionID.create(
                    user_id=user.id,
                    union_id=union_info['unionid'],
                )
            except Exception:
                import traceback
                current_app.logger.error(traceback.format_exc())
                user.delete()
                raise LogicError('创建失败')
            user_id = user.id
        else:
            user = ChatbotUserInfo.get_by_id(user_id)
            user.last_action_ts = datetime.datetime.now()
            user.save()

        token_dict = ChatBotToken.generate_token(user_id)

        data = dict()
        data['user'] = user.to_dict()
        data['token'] = token_dict

        return data

