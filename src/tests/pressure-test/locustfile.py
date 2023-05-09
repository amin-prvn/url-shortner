from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def create_short_url(self):
        url = {"target_url": "https://google.com"}
        headers = {"Content-Type": "application/json"}
        response = self.client.post("/url", json=url, headers=headers)

    @task
    def get_short_url(self):
        response = self.client.get(f"/3AOSX")