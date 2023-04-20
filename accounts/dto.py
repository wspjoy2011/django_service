from datetime import datetime
from typing import NamedTuple


class CustomUserDTO(NamedTuple):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str


class ProfileDTO(NamedTuple):
    avatar: str
    gender: str
    date_of_birth: datetime
    bio: str
    info: str


class UserWithProfileDTO(NamedTuple):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: str
    profile: ProfileDTO


class ActivationTokenDTO(NamedTuple):
    email: str
    token: str


class TokenDTO(NamedTuple):
    id: int
    token: str
    create_at: datetime


class OnlyEmailDTO(NamedTuple):
    email: str


class ReactivateUserTokenDTO(OnlyEmailDTO):
    pass


class RequestPasswordResetTokenDTO(OnlyEmailDTO):
    pass


class PasswordResetTokenDTO(NamedTuple):
    id: int
    token: str
    email: str
    create_at: datetime


class ResetPasswordTokenDTO(NamedTuple):
    email: str
    token: str
    new_password: str

