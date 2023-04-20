from drf_yasg import openapi

register_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="User email"),
        "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="First name"),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last name"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password"),
        "avatar": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="Avatar URL"),
        "gender": openapi.Schema(type=openapi.TYPE_STRING, description="Gender ('male' or 'female')"),
        "date_of_birth": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE,
                                        description="Date of birth (YYYY-MM-DD)"),
        "bio": openapi.Schema(type=openapi.TYPE_STRING, description="Short bio"),
        "info": openapi.Schema(type=openapi.TYPE_STRING, description="Additional information"),
    },
    required=["email", "username", "first_name", "last_name",
              "password", "avatar", "gender", "date_of_birth", "bio", "info"],
)

register_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Registration success message"),
        "token": openapi.Schema(type=openapi.TYPE_STRING, description="Activation token"),
        "user": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL,
                                        description="User email"),
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="First name"),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last name"),
                "avatar": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="Avatar URL"),
                "gender": openapi.Schema(type=openapi.TYPE_STRING, description="Gender ('male' or 'female')"),
                "date_of_birth": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE,
                                                description="Date of birth (YYYY-MM-DD)"),
                "bio": openapi.Schema(type=openapi.TYPE_STRING, description="Short bio"),
                "info": openapi.Schema(type=openapi.TYPE_STRING, description="Additional information"),
            }
        )
    }
)

activate_user_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "token": openapi.Schema(type=openapi.TYPE_STRING, description="Activation token"),
        "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="User email"),
    },
    required=["token", "email"],
)

activate_user_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Activation success message"),
    },
)

reactivate_user_token_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="User email"),
    },
    required=["email"],
)

reactivate_user_token_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Reactivation success message"),
        "token": openapi.Schema(type=openapi.TYPE_STRING, description="New activation token"),
    },
)

request_password_reset_token_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="User email"),
    },
    required=["email"],
)

request_password_reset_token_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Password reset success message"),
    },
)

reset_password_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="User email"),
        "token": openapi.Schema(type=openapi.TYPE_STRING, description="Password reset token"),
        "new_password": openapi.Schema(type=openapi.TYPE_STRING, description="New password (min. 8 characters)"),
    },
    required=["email", "token", "new_password"],
)

reset_password_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Password reset success message"),
    },
)

token_obtain_pair_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="The JWT refresh token"),
        "access": openapi.Schema(type=openapi.TYPE_STRING, description="The JWT access token"),
    },
    required=["refresh", "access"]
)