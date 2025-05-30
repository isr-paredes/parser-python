class Person:
    def __hash__(self):
        return hash(self.name)
