from src.core.handlers.exceptions import *


class DuplicateUserException(DuplicateResourceException):
    pass


class InvalidAdminLoginException(InvalidLoginException):
    pass


class AdminPermissionDeniedException(UnauthorizedAccessException):
    pass


class UsernameTooShortException(UserInputException):
    pass


class UsernameTooLongException(UserInputException):
    pass


class OpeningBalanceException(MinimumBalanceException):
    pass