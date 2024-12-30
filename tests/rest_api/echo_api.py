import requests
from guara.transaction import AbstractTransaction

BASE_URL = "https://postman-echo.com"


class Get(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, path: dict):
        result = ""
        for k, v in path.items():
            result = f"{result}{k}={v}&"
        result = result[:-1]
        return requests.get(f"{BASE_URL}/get?{result}").json()


class Post(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, data):
        return requests.post(url=f"{BASE_URL}/post", data=data).json()
