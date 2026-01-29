from .. import db

"""角色-权限关联表"""
role_permissions = db.Table('role_permissions',
    db.Column('role_name', db.String(80), db.ForeignKey('roles.name'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

"""用户-角色关联表"""
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_name', db.String(80), db.ForeignKey('roles.name'), primary_key=True)
                      )