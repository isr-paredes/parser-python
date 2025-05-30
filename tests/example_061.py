class Reverse:
    def __init__(self, data):
        self.data = data
    def __iter__(self):
        return reversed(self.data)
