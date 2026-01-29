"""这里记录了全部的装饰器"""
from functools import wraps
from flask import g,jsonify
"""权限认证的装饰器"""
def require_permission(permission):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if not hasattr(g, 'current_user') or g.current_user is None:
                return jsonify({'data':'','code': 401, 'msg': '未认证'}), 401

            permission_list = g.current_user.get('permissions',[])

            if permission not in permission_list:
                return jsonify({'data':'','code':40302,'msg':'无权限'}),40302

            return func(*args, **kwargs)

        return wrapper
    return decorator