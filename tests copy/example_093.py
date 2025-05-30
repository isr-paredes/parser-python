class MyList:
    def __init__(self, data):
        self.data = data
    def __getitem__(self, index):
        return self.data[index]
