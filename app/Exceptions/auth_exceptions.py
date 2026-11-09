class AuthAppException(Exception):
    pass 


class InvalidCredentialException(AuthAppException):
    def __init__(self, msg: str = "Could not validate credentials"):
        self.msg = msg
        super().__init__(msg)


class EmailAlreadyExistException(AuthAppException):
    def __init__(self, msg: str = "This email is already registered"):
        self.msg = msg 
        super().__init__(msg) 
