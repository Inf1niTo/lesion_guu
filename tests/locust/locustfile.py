from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Интервал между запросами

    @task(1)
    def get_home_page(self):
        self.client.get("/")  # Главная страница

    @task(2)
    def get_nocodb_data(self):
        self.client.get("/nocodb-data/")  # Данные с NocoDB

    @task(3)
    def get_users(self):
        self.client.get("/users/")  # Получение всех пользователей

    @task(4)
    def get_swagger_docs(self):
        self.client.get("/api/docs/")  # Документация Swagger UI

    @task(5)
    def post_data(self):
        self.client.post("/nocodb-data/", json={"key": "value"})  # Пример POST-запроса

    @task(6)
    def get_admin_page(self):
        self.client.get("/admin/")  # Страница админки
