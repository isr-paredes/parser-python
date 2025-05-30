class Person:
    @classmethod
    def from_birth_year(cls, name, year):
        from datetime import date
        age = date.today().year - year
        return cls(name, age)
