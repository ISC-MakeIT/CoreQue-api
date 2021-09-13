class Route:
    def __init__(self):
        self.handlers = {}

    def add(self, path: str, func: callable) -> None:
        self.handlers[path] = func

    def run(self, path: str) -> None:
        if path in self.handlers:
            self.handlers[path]()
        else:
            print("404")
