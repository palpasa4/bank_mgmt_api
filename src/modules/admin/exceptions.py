from src.core.handlers.exceptions import *


class DuplicateUserException(DuplicateResourceException): ...


class InvalidAdminLoginException(AuthException): ...


class AdminPermissionDeniedException(PermissionDeniedException): ...
