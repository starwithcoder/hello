"""这是是全部的中间件"""
from flask import g ,request,jsonify
from datetime import datetime
import jwt
import os
#默认设置五个权限分别是司机，汽车，记录，事故，其他，默认对应0，1，2，3，4
#由于开发原因以下权限注释
# PROTECTED_ROUTES = {
#     # 用户管理 - 其他(4) - 排除登录
#     'POST:/api/register': 4,
#
#     # 司机管理 - 司机(0)
#     'GET:/api/drivers/': 0,
#     'POST:/api/drivers/': 0,
#     'PUT:/api/drivers/': 0,
#     'DELETE:/api/drivers/': 0,
#
#     # 车辆管理 - 汽车(1)
#     'GET:/api/cars/': 1,
#     'POST:/api/cars/': 1,
#     'PUT:/api/cars/': 1,
#     'DELETE:/api/cars/': 1,
#
#     # 车辆变更 - 记录(2)
#     'GET:/api/vehicle_change/': 2,
#     'POST:/api/vehicle_change/add': 2,
#     'PUT:/api/vehicle_change/edit/': 2,
#     'DELETE:/api/vehicle_change/delete/': 2,
#
#     # 司机归还 - 记录(2)
#     'POST:/api/driver_return/add': 2,
#     'GET:/api/driver_return/search': 2,
#     'PUT:/api/driver_return/': 2,
#     'DELETE:/api/driver_return/': 2,
#
#     # 事故记录 - 事故(3)
#     'POST:/api/accident_record/': 3,
#     'GET:/api/accident_record/': 3,
#     'PUT:/api/accident_record/': 3,
#     'DELETE:/api/accident_record/': 3,
#
#     # 车辆动态 - 事故(3)
#     'POST:/api/vehicle_dynamic/': 3,
#     'GET:/api/vehicle_dynamic/': 3,
#     'PUT:/api/vehicle_dynamic/': 3,
#     'DELETE:/api/vehicle_dynamic/': 3,
#
#     # 车辆收据记录 - 记录(2)
#     'POST:/api/carReceiptRecord/': 2,
#     'GET:/api/carReceiptRecord/': 2,
#     'PUT:/api/carReceiptRecord/': 2,
#     'DELETE:/api/carReceiptRecord/': 2,
#
#     # 权限管理 - 其他(4)
#     'GET:/api/permissions/get': 4,
#     'POST:/api/permissions/post': 4,
#     'PUT:/api/permissions/update': 4,
#     'DELETE:/api/permissions/delete': 4,
#
#     # 角色管理 - 其他(4)
#     'GET:/api/roles/get': 4,
#     'POST:/api/roles/post': 4,
#     'PUT:/api/roles/put': 4,
#     'DELETE:/api/roles/delete': 4,
# }
def register_auth_middleware(app):
    @app.before_request
    def load_user_from_token():
        print('中间件token')
        auth  = request.headers.get('Authorization','')
        #如果有token,解析token并存入到全局数据中
        if auth.startswith('Bearer '):
            auth_token = auth.split(' ')[1]
            print(datetime.now())

            try:
                #解析token
                payload = jwt.decode(auth_token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])
                #存入全局数据
                g.current_user = payload
                return None
            except jwt.InvalidTokenError as e:
                return jsonify({'code': 401, 'msg': '无效的token'}), 401
        else:
            print('没有token')
            #没有token
            g.current_user = None
            return None


    #@app.before_request
    # def check_permission():
    #     if g.current_user is None:
    #         return None
    #
    #     route_key = f"{request.method}:{request.path}"
    #     required_permission = PROTECTED_ROUTES.get(route_key)
    #     print(route_key)
    #     if required_permission:
    #         permission_list = g.current_user.get('permissions', [])
    #         print(permission_list)
    #         print(required_permission)
    #         if required_permission not in permission_list:
    #             return jsonify({
    #                 'data': '',
    #                 'code': 403,
    #                 'msg': f'无权限访问，需要权限: {required_permission}'
    #             }), 403
    #     return None