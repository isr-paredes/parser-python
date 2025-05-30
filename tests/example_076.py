class Meta(type):
    def __new__(cls, name, bases, dct):
        dct['id'] = 1
        return super().__new__(cls, name, bases, dct)

class MyClass(metaclass=Meta):
    pass
