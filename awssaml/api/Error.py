class Error(Exception):
    """Base class for awssaml errors"""
    pass


class IncorrectAssertionError(Error):
    def __init__(self, message):
        self.message = message
