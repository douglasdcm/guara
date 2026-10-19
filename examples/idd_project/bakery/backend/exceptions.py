# ==========================================================
# ERRORS / RULES
# ==========================================================


class DatabaseErrorItemNotFound(Exception):
    pass


class BusinessError(Exception):
    pass


class UserAlreadyCreated(Exception):
    pass


class UserAlreadyLogged(Exception):
    pass


class DuplicateProduct(BusinessError):
    pass


class ProductNotFound(BusinessError):
    pass


class InsufficientStock(BusinessError):
    pass


class ProductExpired(BusinessError):
    pass


class CashAlreadyOpen(BusinessError):
    pass


class CashAlreadyClosed(BusinessError):
    pass


class PermissionDenied(BusinessError):
    pass
