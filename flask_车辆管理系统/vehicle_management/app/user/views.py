from flask import Blueprint, request, jsonify,g
from werkzeug.security import generate_password_hash, check_password_hash
from vehicle_management.models import User
from vehicle_management.app.user import user_bp
from vehicle_management import db
import jwt
from datetime import datetime,  timedelta,timezone
import os
import logging
#登录成功以后进行token的书写
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
def get_token(username,role,permissions):


    payload ={
        'username':username,
        'role':role,
        'permissions':permissions,
        'exp':datetime.now(timezone.utc)+timedelta(hours=24),

    }

    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
#登录验证
def authenticate_user(username,password):

    if not username or not password:
        return jsonify({'code': 40401, 'msg': '缺少用户名或密码'})
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401
    role = user.role_name
    permissions = [p.id for p in user.role.permissions]
    token = get_token(username, role, permissions)
    return jsonify({'status': 200, 'msg': 'success', 'user_id': user.id, 'token': token}), 200

logger = logging.getLogger(__name__)

@user_bp.route('login', methods=['POST'])
def login():
    logger.info("===== login =====")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    logger.debug(username)
    # 如果纯在token

    return authenticate_user(username,password)
    #如果不存在
    # else:
    #     print('无token')
    #     return authenticate_user(username,password)


@user_bp.route('register', methods=['POST'])
def register():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    # 接收表单数据
    if not role:
        role = "user"

    if not username or not password:
        return jsonify({'code': 400001, 'msg': '缺少用户名或密码'})

    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'code': 40009, 'msg': '用户名已存在'})

    # 创建新用户
    
    new_user = User( username=username, password_hash = generate_password_hash(password),role_name = role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status': 201, 'msg': '注册成功', 'user_id': new_user.id}), 201


