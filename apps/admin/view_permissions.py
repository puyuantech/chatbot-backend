from flask import request
from flask_restful import fields, marshal_with
from models import Permission, RolePermissionMap
from bases.viewhandler import ApiViewHandler
from utils.helper import generate_sql_pagination
from utils.decorators import params_required, super_admin_login_required


class PermissionsAPI(ApiViewHandler):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'url': fields.String,
        'menu': fields.String,
    }

    @super_admin_login_required
    def get(self):
        p = generate_sql_pagination()
        query = Permission.filter_by_query(is_super_admin=False)
        return p.paginate(query)

    @marshal_with(resource_fields)
    @super_admin_login_required
    @params_required(*['name', 'url', 'menu'])
    def post(self):
        instance = Permission.create(
            name=self.input.name,
            url=self.input.url,
            menu=self.input.menu,
        )
        return instance


class PermissionAPI(ApiViewHandler):

    @super_admin_login_required
    def get(self, _id):
        instance = Permission.get_by_id(_id)
        return instance.to_dict()

    @super_admin_login_required
    def put(self, _id):
        obj = Permission.get_by_id(_id)
        columns = {i: request.json.get(i) for i in ['name', 'menu']}
        for i in columns:
            if columns[i]:
                obj.update(commit=False, **{i: columns[i]})
        obj.save()
        return obj

    @super_admin_login_required
    def delete(self, _id):
        RolePermissionMap.filter_by_query(
            show_deleted=True,
            permission_id=_id,
        ).delete()
        obj = Permission.get_by_id(_id)
        obj.delete()

