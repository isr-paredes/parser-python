class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_birth_year(cls, name, year):
        from datetime import date
        age = date.today().year - year
        return cls(name, age)
