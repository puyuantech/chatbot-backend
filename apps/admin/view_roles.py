
from flask import request
from flask_restful import fields, marshal_with
from models import Role, RolePermissionMap, UserRoleMap
from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from utils.helper import generate_sql_pagination
from utils.decorators import params_required, super_admin_login_required
from .libs.permissions import update_role_permission


class RolesAPI(ApiViewHandler):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
    }

    @super_admin_login_required
    def get(self):
        p = generate_sql_pagination()
        query = Role.filter_by_query()
        roles = p.paginate(query)
        return roles

    @marshal_with(resource_fields)
    @super_admin_login_required
    @params_required(*['name'])
    def post(self):
        if Role.filter_by_query(name=self.input.name).first():
            raise VerifyError(f'{self.input.name} 已经存在')
        role = Role.create(
            name=self.input.name,
        )
        role = update_role_permission(role)
        return role


class RoleAPI(ApiViewHandler):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'permissions': fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        }),
    }

    @marshal_with(resource_fields)
    @super_admin_login_required
    def get(self, _id):
        obj = Role.get_by_id(_id)
        return obj

    @marshal_with(resource_fields)
    @super_admin_login_required
    def put(self, _id):
        obj = Role.get_by_id(_id)
        columns = {i: request.json.get(i) for i in ['name']}
        for i in columns:
            if columns[i]:
                obj.update(commit=False, **{i: columns[i]})
        obj.save()
        obj = update_role_permission(obj)
        return obj

    @super_admin_login_required
    def delete(self, _id):
        UserRoleMap.filter_by_query(show_deleted=True, role_id=_id).delete()
        obj = Role.get_by_id(_id)
        obj.delete()


class RolePermission(ApiViewHandler):

    @super_admin_login_required
    @params_required(*['role_id', 'permission_id'])
    def post(self):
        RolePermissionMap.create(
            role_id=self.input.role_id,
            permission_id=self.input.permission_id,
        )

    @super_admin_login_required
    @params_required(*['role_id', 'permission_id'])
    def delete(self):
        obj = RolePermissionMap.get_by_query(
            role_id=self.input.role_id,
            permission_id=self.input.permission_id,
        )
        obj.delete()


