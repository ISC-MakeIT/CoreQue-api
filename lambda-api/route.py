from writer import Writer


class Route:
    def __init__(self, writer: Writer = None, handlers: dict = {}) -> None:
        self.__handlers = handlers
        self.__writer = writer

    def add(self, path: str, func: callable) -> None:
        self.__handlers[path] = func

    def has_path(self, path: str) -> bool:
        return path in self.__handlers

    def run(self, path: str) -> bool:
        if self.has_path(path):
            if self.__writer is not None:
                self.__writer.body_write(self.__handlers[path]())
            else:
                self.__handlers[path]()
            return True
        return False

    def get_result(self) -> dict:
        return self.__writer.get_response()
