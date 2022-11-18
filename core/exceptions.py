class BadCredentialsError(Exception):
    pass


class TokenExpirateError(Exception):
    pass


class TokenInvalidError(Exception):
    pass


class UnAuthorizedError(Exception):
    pass


class DbConnectionError(Exception):
    pass