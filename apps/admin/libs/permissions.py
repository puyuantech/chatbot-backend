from flask import request
from models import RolePermissionMap


def update_role_permission(role):
    add_permission_ids = request.json.get('add_permission_ids')
    del_permission_ids = request.json.get('del_permission_ids')

    if add_permission_ids:
        for permission_id in add_permission_ids:
            RolePermissionMap.create(
                role_id=role.id,
                permission_id=permission_id,
            )
    if del_permission_ids:
        for permission_id in del_permission_ids:
            obj = RolePermissionMap.get_by_query(
                role_id=role.id,
                permission_id=permission_id,
            )
            obj.delete()
    return role

