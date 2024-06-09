from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        response = self.client.post("/session/start")
        self.session_id = response.json()["session_id"]

    @task(1)
    def send_message(self):
        self.client.post("/message", json={"session_id": self.session_id, "message": "Hello"})

    @task(2)
    def get_history(self):
        self.client.get(f"/session/{self.session_id}/history")

    @task(3)
    def end_session(self):
        self.client.post("/session/end", json={"session_id": self.session_id})

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 9)

if __name__ == "__main__":
    import locust
    locust.run()
