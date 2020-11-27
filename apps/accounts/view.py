
from flask import g, request
from flask_restful import fields, marshal_with
from models import User, Permission, Token
from bases.globals import db
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError, LogicError
from utils.decorators import params_required, login_required
from extensions.s3.head_img_store import HeadImgStore


class SelfPermission(ApiViewHandler):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'url': fields.String,
        'menu': fields.String,
    }

    @marshal_with(resource_fields)
    @login_required
    def get(self):
        if g.user.role_id == 1:
            return Permission.filter_by_query().all()
        data = {}
        for i in g.user.roles:
            for j in i.permissions:
                data[j.id] = j
        return list(data.values())


class UpLoadHeadImg(ApiViewHandler):
    @login_required
    def post(self):
        """上传头像"""
        file_obj = request.files.get('file')
        if not file_obj:
            raise VerifyError('没有图片！')
        status, img = HeadImgStore.store_head_img_from_user(g.user.id, file_obj)
        if not status:
            raise LogicError('store head img failed! (err_msg){}'.format(img))
        return {
            'avatar_url': img
        }


class ResetPassword(ApiViewHandler):
    @params_required(*['password', 'new_password'])
    @login_required
    def post(self):
        if not self.is_valid_password(self.input.new_password):
            raise VerifyError('密码应该包含至少一个数字和一个字母，且长度在8-16之间。')
        if not g.user_login.check_password(self.input.password):
            raise VerifyError('原始密码错误！')
        g.user_login.password = self.input.new_password
        g.user_login.save()
        Token.filter_by_query(show_deleted=True, user_id=g.user.id).delete()
        db.session.commit()


class ChangeAPI(ApiViewHandler):
    @login_required
    def post(self):
        columns = {i: request.json.get(i) for i in [
            'nick_name',
            'sex',
            'email',
            'avatar_url',
            'site',
        ]}
        user_info = User.filter_by_query(user_id=g.user.id).first()
        for i in columns:
            if columns[i]:
                user_info.update(commit=False, **{i: columns[i]})
        user_info.save()

