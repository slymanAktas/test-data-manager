class MockException(BaseException):
    """ Common base class for all non-exit exceptions. """

    def __init__(self, *message):
        self.message = '!! Has Mock Url  On CREDITCARDTYPE_CONFIGPARAMSMAP Table,Please Check CONFIGVALUE Field' if message == () else \
            message[0]


class RunPathExeption(BaseException):
    def __init__(self, *message):
        self.message = '!! Please check your run path ' if message == () else \
            message[0]
