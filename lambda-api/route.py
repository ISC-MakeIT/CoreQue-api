from writer import Writer


class Route:
    def __init__(self, writer: Writer = None, handlers: dict = {}) -> None:
        self.__handlers = handlers
        self.__writer = writer

    def add(self, path: str, func: callable) -> None:
        self.__handlers[path] = func

    def has_path(self, path: str) -> bool:
        return path in self.__handlers

    def run(self, path: str, params: dict = None) -> bool:
        if not self.has_path(path):
            return False
        if params is None:
            if self.__writer is None:
                self.__handlers[path]()
                return True
            self.__writer.body_write(self.__handlers[path]())
        else:
            if self.__writer is None:
                self.__handlers[path](params)
                return True
            self.__writer.body_write(self.__handlers[path](params))
        return True

    def get_result(self) -> dict:
        return self.__writer.get_response()
