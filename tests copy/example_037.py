class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)
