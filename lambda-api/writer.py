class Writer:
    def __init__(self, response: dict = {}) -> None:
        self.__response = response

    def get_response(self) -> dict:
        if "statusCode" not in self.__response:
            self.__response["statusCode"] = 200
        return self.__response

    def body_write(self, body: str) -> None:
        self.__response["body"] = body
