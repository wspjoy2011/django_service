from typing import Union

from rest_framework_simplejwt.authentication import JWTAuthentication

from api.exceptions import ForbiddenException, UnauthorizedException
from blog.dto import PostDTO, CommentDTO


class JWTPermissionValidator:
    @classmethod
    def validate_jwt_authentication_or_raise(cls, request):
        """Check jwt token and authenticate"""
        jwt_auth = JWTAuthentication()
        header = jwt_auth.get_header(request)
        if header is None:
            raise UnauthorizedException()

        return jwt_auth.authenticate(request)

    @classmethod
    def is_superuser_or_raise(cls, request):
        """Check permission to only allow superuser."""
        user, _ = cls.validate_jwt_authentication_or_raise(request)
        if not user.is_superuser:
            raise ForbiddenException("only superuser allow")

    @classmethod
    def is_superuser_or_object_author_or_raise(cls, request, object_dto: Union[PostDTO, CommentDTO]):
        """Check permission to only allow post author or superuser to update object."""
        user, _ = cls.validate_jwt_authentication_or_raise(request)
        if not (object_dto.author_id == user.id or user.is_superuser):
            raise ForbiddenException("only superuser or object owner allow")
