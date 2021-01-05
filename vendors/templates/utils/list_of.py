class _ListOfValidator:
    """attrs用のバリデータ
    参考: https://github.com/python-attrs/attrs/blob/master/src/attr/validators.py
    """

    def __init__(self, type):
        self.type = type

    def __call__(self, inst, attr, value):
        for v in value:
            if not isinstance(v, self.type):
                raise TypeError(f"{type(v)} is not a subclass of {self.type}")

    def __repr__(self):
        return f"<list_of validator for type {type}>"


def list_of(type):
    return _ListOfValidator(type)