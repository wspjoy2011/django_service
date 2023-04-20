from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.dto import ProfileDTO, UserWithProfileDTO
from accounts.validators import validate_birth_date


class CustomUserDTOSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class ProfileDTOSerializer(serializers.Serializer):
    avatar = serializers.URLField()
    gender = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    date_of_birth = serializers.DateField(validators=[validate_birth_date])
    bio = serializers.CharField()
    info = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class UserWithProfileDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profile = ProfileDTOSerializer()

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        profile_dto = ProfileDTO(**profile_data)
        user_with_profile_dto = UserWithProfileDTO(profile=profile_dto, **validated_data)
        return user_with_profile_dto

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class ActivationTokenDTOSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class ReactivateUserTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class RequestPasswordResetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class ResetPasswordTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        self.user = authenticate(**{
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        })

        if not self.user:
            raise serializers.ValidationError(
                'No active account found with the given credentials',
                code='authentication',
            )

        refresh = self.get_token(self.user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        if 'returnSecureToken' in self.context:
            data['returnSecureToken'] = self.context['returnSecureToken']

        return data

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        return token

    def create(self, validated_data):
        raise NotImplementedError("This serializer should not be used to create instances.")

    def update(self, instance, validated_data):
        raise NotImplementedError("This serializer should not be used to update instances.")


class TokenObtainPairResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError("This serializer should not be used to create instances.")

    def update(self, instance, validated_data):
        raise NotImplementedError("This serializer should not be used to update instances.")


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError("This serializer should not be used to create instances.")

    def update(self, instance, validated_data):
        raise NotImplementedError("This serializer should not be used to update instances.")
