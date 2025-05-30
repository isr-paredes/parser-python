class Decorator:
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        print("Decorated!")
        return self.func(*args, **kwargs)
