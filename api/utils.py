from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user_id_from_token(request):
    auth = JWTAuthentication()
    try:
        auth_header = request.headers['Authorization']
        access_token = auth_header.split(' ')[-1]
    except (KeyError, IndexError):
        return None

    validated_token = auth.get_validated_token(access_token)
    payload = validated_token.payload

    user_id = payload.get('user_id')

    return user_id
