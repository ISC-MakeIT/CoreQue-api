class Route:
    def __init__(self):
        self.__handlers = {}

    def add(self, path: str, func: callable) -> None:
        self.__handlers[path] = func

    def has_path(self, path: str) -> bool:
        return path in self.__handlers

    def run(self, path: str) -> bool:
        if self.has_path(path):
            self.__handlers[path]()
            return True
        return False
