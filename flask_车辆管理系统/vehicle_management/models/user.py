from .. import db
from .associations import user_roles

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)


    role_name = db.Column(db.String(80), db.ForeignKey('roles.name'), nullable=False)
    role = db.relationship('Role', back_populates='users')