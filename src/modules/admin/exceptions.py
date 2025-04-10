from src.core.handlers.exceptions import InvalidLoginException,DuplicateResourceException


class DuplicateUserException(DuplicateResourceException):
    pass


class InvalidAdminLoginException(InvalidLoginException):
    pass


