from flask import request, g
from models import User, UserLogin
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError, LogicError
from utils.helper import generate_sql_pagination
from utils.decorators import params_required, super_admin_login_required, login_required, permission_required
from extensions.s3.head_img_store import HeadImgStore
from .libs.staff import get_all_user_info_by_user, update_user_info
from .libs.users import register_user


class UsersAPI(ApiViewHandler):

    @login_required
    @permission_required('用户管理')
    def get(self):
        p = generate_sql_pagination()
        query = User.filter_by_query(is_staff=False)
        data = p.paginate(query, call_back=lambda x: [get_all_user_info_by_user(i) for i in x])
        return data

    @login_required
    @permission_required('用户管理')
    @params_required(*['username', 'password'])
    def post(self):
        # 创建用户
        user, user_login = register_user(
            self.input.username,
            self.input.password,
        )

        # 添加用户信息
        update_user_info(user)
        return 'success'


class UserAPI(ApiViewHandler):

    @super_admin_login_required
    def get(self, _id):
        instance = User.get_by_id(_id)
        return get_all_user_info_by_user(instance)

    @super_admin_login_required
    def put(self, _id):
        user = User.get_by_id(_id)
        user = update_user_info(user)
        return get_all_user_info_by_user(user)

    @super_admin_login_required
    def delete(self, _id):
        user = User.get_by_id(_id)
        user_login = UserLogin.filter_by_query(user_id=user.id).first()
        user.logic_delete()
        if user_login:
            user_login.logic_delete()


class ResetUserPassword(ApiViewHandler):

    @login_required
    def put(self, _id):
        password = request.json.get('password')
        password = password if password else '123456'
        user = User.get_by_id(_id)
        user_login = UserLogin.filter_by_query(user_id=user.id).one()
        user_login.password = password
        user_login.save()
        return 'success'


class UpLoadHeadImg(ApiViewHandler):
    @login_required
    def post(self, _id):
        """上传用户头像"""
        file_obj = request.files.get('file')
        if not file_obj:
            raise VerifyError('没有图片！')
        status, img = HeadImgStore.store_head_img_from_user(_id, file_obj)
        if not status:
            raise LogicError('store head img failed! (err_msg){}'.format(img))
        return {
            'avatar_url': img
        }

