class Route:
    def __init__(self):
        self.handlers = {}

    def add(self, path: str, func: callable) -> None:
        self.handlers[path] = func
