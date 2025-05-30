class MyList:
    def __init__(self, data):
        self.data = data
    def __contains__(self, item):
        return item in self.data
