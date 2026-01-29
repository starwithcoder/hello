"""这是是全部的中间件"""
from flask import g ,request,jsonify
from datetime import datetime
import jwt
import os
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

                payload = jwt.decode(auth_token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])

                g.current_user = payload
                return None
            except jwt.InvalidTokenError as e:
                return str(e)
        else:
            print('没有token')
            #没有token
            g.current_user = None
            return None
