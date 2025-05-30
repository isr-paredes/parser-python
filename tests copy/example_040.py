class Counter:
    def __iter__(self):
        self.n = 0
        return self
    def __next__(self):
        self.n += 1
        if self.n > 5:
            raise StopIteration
        return self.n
