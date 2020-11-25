from flask import Blueprint
from flask_restful import Api
from .view_roles import RoleAPI, RolesAPI, RolePermission
from .view_permissions import PermissionAPI, PermissionsAPI
from .view_staffs import StaffsAPI, StaffAPI, StaffRole, ResetStaffPassword, UpLoadHeadImg
from .view_users import UsersAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/admin')
api = Api(blu)

api.add_resource(RolesAPI, '/roles')
api.add_resource(RoleAPI, '/role/<int:_id>')
api.add_resource(RolePermission, '/role/permission')

api.add_resource(PermissionsAPI, '/permissions')
api.add_resource(PermissionAPI, '/permission/<int:_id>')

api.add_resource(StaffsAPI, '/staffs')
api.add_resource(StaffAPI, '/staff/<int:_id>')
api.add_resource(StaffRole, '/staff/role')
api.add_resource(ResetStaffPassword, '/staff/reset_password/<int:_id>')
api.add_resource(UpLoadHeadImg, '/staff/upload_head_img/<int:_id>')

api.add_resource(UsersAPI, '/users')


