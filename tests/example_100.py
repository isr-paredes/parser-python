class Person:
    def __format__(self, format_spec):
        if format_spec == 'short':
            return self.name
        else:
            return f"{self.name} ({self.age})"
