class Route:
    def __init__(self):
        self.handlers = {}

    def add(self, path, func):
        self.handlers[path] = func
