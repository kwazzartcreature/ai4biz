class ExpiredTokenException(Exception):
    def __init__(self, message="Token has expired"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenException(Exception):
    def __init__(self, message="Invalid token"):
        self.message = message
        super().__init__(self.message)
