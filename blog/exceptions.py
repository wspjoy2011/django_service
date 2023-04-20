from django.core.exceptions import ValidationError


class CategoryAlreadyExistsError(ValidationError):
    def __init__(self, message="Category with this name or slug already exists", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class CategoryDoesNotExistsError(ValidationError):
    def __init__(self, message="Category not exists", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class PostDoesNotExistsError(ValidationError):
    def __init__(self, message="Post not exists", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class PostCommentDoesNotExistsError(ValidationError):
    def __init__(self, message="Post comment not exists", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
