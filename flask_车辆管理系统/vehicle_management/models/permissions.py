from .associations import role_permissions
from .. import  db


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    roles = db.relationship('Role',secondary=role_permissions,back_populates='permissions')

    description = db.Column(db.Text)