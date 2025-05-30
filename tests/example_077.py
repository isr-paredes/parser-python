class MyClass:
    def __new__(cls):
        print("Creating instance")
        return super().__new__(cls)
