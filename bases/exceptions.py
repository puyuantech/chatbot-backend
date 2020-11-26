

class BaseError(Exception):
    def __init__(self, msg):
        self.code = 1001
        self.msg = msg
        self.status = 200

    def __str__(self):
        return self.msg


class AuthError(BaseError):
    def __init__(self, msg):
        self.code = 1002
        self.msg = msg
        self.status = 401


class AuthPermissionError(BaseError):
    def __init__(self, msg):
        self.code = 1002
        self.msg = msg
        self.status = 403


class VerifyError(BaseError):
    def __init__(self, msg):
        super(VerifyError, self).__init__(msg)
        self.code = 1003
        self.status = 400


class LogicError(BaseError):
    def __init__(self, msg):
        self.code = 1004
        self.msg = msg
        self.status = 400


class ParamsError(BaseError):
    def __init__(self, msg):
        self.code = 1005
        self.msg = msg
        self.status = 400

