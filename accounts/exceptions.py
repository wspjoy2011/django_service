from django.core.exceptions import ValidationError


class UserAlreadyExistsError(ValidationError):
    def __init__(self, message="User with this email or username already exists", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class UserAlreadyActivatedError(ValidationError):
    def __init__(self):
        super().__init__("User is already activated")


class UserTokenNotFoundError(ValidationError):
    def __init__(self, message="User token not found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class UserNotActivatedError(ValidationError):
    def __init__(self, message="User is not activated", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class UserNotFoundError(ValidationError):
    def __init__(self, message="User not found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class TokenExpiredError(ValidationError):
    def __init__(self, message="Token expired, reactivate token", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class InvalidTokenError(ValidationError):
    def __init__(self, message="Invalid token", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class WeakPasswordError(ValidationError):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, **kwargs)




