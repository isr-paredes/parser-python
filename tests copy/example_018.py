class Dog:
    @property
    def name(self):
        return self._name

    @name.deleter
    def name(self):
        del self._name
