from writer import Writer


class Route:
    def __init__(self, writer: Writer = None, handlers: dict = {}) -> None:
        self.__handlers = handlers
        self.__writer = writer

    def add(self, path: str, func: callable, key: str = None) -> None:
        if key is not None:
            self.__handlers[path] = {"key": key, "func": func}
        else:
            self.__handlers[path] = {"key": None, "func": func}

    def has_path(self, path: str) -> bool:
        return path in self.__handlers

    def run(self, path: str, param: dict = None) -> bool:
        if not self.has_path(path):
            return False
        if param is None:
            if self.__writer is None:
                self.__handlers[path]["func"]()
                return True
            self.__writer.body_write(self.__handlers[path]["func"]())
        else:
            key = self.__handlers[path]["key"]
            if self.__writer is None:
                self.__handlers[path]["func"](param[key])
                return True
            self.__writer.body_write(self.__handlers[path]["func"](param[key]))
        return True

    def get_result(self) -> dict:
        return self.__writer.get_response()
