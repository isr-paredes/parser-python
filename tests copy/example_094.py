class MyList:
    def __init__(self, data):
        self.data = data
    def __setitem__(self, index, value):
        self.data[index] = value
