from src.core.exceptions import *


class DuplicateUserException(DuplicateResourceException): ...


class InvalidAdminLoginException(AuthException): ...


class AdminPermissionDeniedException(PermissionDeniedException): ...
