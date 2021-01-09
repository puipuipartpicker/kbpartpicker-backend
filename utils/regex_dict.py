import re


class RegexDict(dict):
    
    def __init__(self):
        super(RegexDict, self).__init__()

    def __getitem__(self, item):
        for k, v in self.items():
            if k.search(item):
                return v
        raise KeyError
