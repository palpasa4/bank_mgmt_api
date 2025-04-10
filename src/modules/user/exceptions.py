from src.core.handlers.exceptions import *


class InvalidUserLoginException(InvalidLoginException):
    pass


class UserPermissionDeniedException(UnauthorizedAccessException):
    pass


class WithdrawBalanceException(MinimumBalanceException):
    pass


class DepositBalanceException(MinimumBalanceException):
    pass