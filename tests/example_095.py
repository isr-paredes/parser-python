class MyList:
    def __init__(self, data):
        self.data = data
    def __delitem__(self, index):
        del self.data[index]
