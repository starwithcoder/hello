
from .. import db
from .associations import role_permissions



class Role(db.Model):

    __tablename__ = 'roles'
    name = db.Column(db.String(80), primary_key=True)

    description = db.Column(db.Text,)

    permissions = db.relationship('Permission', secondary=role_permissions,back_populates='roles')

    users = db.relationship('User', back_populates='role',lazy='select')

