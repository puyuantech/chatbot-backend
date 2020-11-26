
from bases.dbwrapper import BaseModel, db


class UserRoleMap(BaseModel):
    __tablename__ = 'map_user_role'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        comment='主键ID',
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        comment='用户ID',
    )
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id'),
        nullable=False,
        comment='角色ID',
    )


class RolePermissionMap(BaseModel):
    __tablename__ = 'map_role_permission'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        comment='主键ID',
    )
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id'),
        nullable=False,
        comment='角色ID',
    )
    permission_id = db.Column(
        db.Integer,
        db.ForeignKey('permissions.id'),
        nullable=False,
        comment='权限ID',
    )


class Permission(BaseModel):
    """
    路由权限
    """
    __tablename__ = 'permissions'

    id = db.Column(
        db.Integer,
        primary_key=True,
        comment='主键ID',
    )
    name = db.Column(
        db.String(127),
        comment='名称',
    )
    url = db.Column(
        db.String(127),
        nullable=False,
        comment='路由',
    )
    menu = db.Column(
        db.String(63),
        nullable=False,
        comment='菜单',
    )
    is_super_admin = db.Column(
        db.BOOLEAN,
        default=False,
        comment='超级管理员独有'
    )


class Role(BaseModel):
    """角色"""
    __tablename__ = 'roles'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        comment='角色ID',
    )
    name = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        comment='角色名',
    )
    permissions = db.relationship(
        'Permission',
        secondary='map_role_permission',
        backref='role',
    )

    def to_normal_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

