class MissingJWT(Exception):
    def __init__(self, message="You are not logged in."):
            self.message = message
            super().__init__(self.message)