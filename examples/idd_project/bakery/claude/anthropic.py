import random


class Text:
    def __init__(self):
        self._type = None
        self._name = None
        self._text = None
        self._input = None
        number = random.randint(1, 10)
        if number > 5:
            self._type = "text"
            self._text = """{
                "items": [{"product": "pao", "quantity": 2}],
                "customer": "joao",
                "discount": 0.1,
                "payments": {
                    "money": 1,
                    "card": 3
                },
                "delivery": "false"
            }"""
        else:
            self._type = "tool_use"
            number = random.randint(1, 10)
            number = 7
            if 1 <= number <= 3:
                self._name = "get_product_info"
                self._input = {"name": "pao"}
            if 3 < number <= 6:
                self._name = "check_stock"
                self._input = {"name": "pao", "quantity": 2}
            if 6 < number < 10:
                self._name = "calculate_total"
                self._input = {"items": [{"p": 1, "q": 1}, {"p": 2, "q": 2}]}
            else:
                # Hallucination
                self._name = "drop_table"

    @property
    def input(self):
        return self._input

    @property
    def name(self):
        return self._name

    @property
    def text(self):
        return self._text

    @property
    def type(self):
        return self._type


class Response:
    @property
    def content(self):
        return [Text()]


class Messages:
    def create(self, *args, **kwargs):
        return Response()


class Anthropic:
    def __init__(self, api_key):
        pass

    @property
    def messages(self):
        return Messages()
