class Person:
    def __lt__(self, other):
        return self.age < other.age
