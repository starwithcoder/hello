from locust import HttpUser, task, between

class MyUser(HttpUser):

    # def on_start(self):
        # 先登录获取 token

        # resp = self.client.post(
        #     "/api/login",
        #     json={"user": "user", "pwd": "123456"}
        # ).json()
        #
        # print("=== 登录响应 ===")
        #
        # print("响应体:", resp.data)  # 关键！看实际返回什么
        # print("================")
        #
        @task
        def get_data(self):
            # 在 Header 中携带 token
            resp =self.client.post('/api/login', json={'username': 'user', 'password': '123456'})
            print(resp)