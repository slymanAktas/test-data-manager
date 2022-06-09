class StringUtils:

    def __init__(self):
        self.__inital_str: str = ""

    @classmethod
    def init(cls):
        return cls()

    def append(self, appended_str):
        self.__inital_str += f" {appended_str}"
        return self

    @property
    def join(self):
        return self.__inital_str[1:]

