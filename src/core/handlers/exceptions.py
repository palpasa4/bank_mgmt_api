class BaseApiException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class DuplicateResourceException(BaseApiException):
    def __init__(self, message: str , status_code: int = 400):
        super().__init__(message, status_code)


class InvalidLoginException(BaseApiException): 
    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, status_code)


class UnauthorizedAccessException(BaseApiException):
    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code)


class UserInputException(BaseApiException):
    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code)


class MinimumBalanceException(BaseApiException):
    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code)


class DatabaseException(BaseApiException):
    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code)
