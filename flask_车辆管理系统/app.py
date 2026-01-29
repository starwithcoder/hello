from vehicle_management import create_app
from flask_cors import CORS

# 创建应用实例
app = create_app()




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
