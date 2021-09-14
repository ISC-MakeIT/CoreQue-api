import json


class Writer:
    def __init__(self, response: dict = {}) -> None:
        self.__response = response

    def get_response(self) -> dict:
        if "statusCode" not in self.__response:
            self.__response["statusCode"] = 200
        return self.__response

    def body_write(self, body: str or dict) -> None:
        if type(body) is dict:
            self.__response["body"] = json.dumps(obj=body)
        else:
            self.__response["body"] = body
