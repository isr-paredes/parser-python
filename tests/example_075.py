class Final(type):
    def __new__(mcs, name, bases, namespace):
        for base in bases:
            if isinstance(base, Final):
                raise TypeError("Cannot subclass final class")
        return super().__new__(mcs, name, bases, namespace)

class Base(metaclass=Final):
    pass
