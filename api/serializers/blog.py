from rest_framework import serializers
from rest_framework.exceptions import ValidationError

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published')
)


class CategoryDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class NewCategoryDTOSerializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class PostDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.SlugField()
    author = serializers.CharField()
    author_id = serializers.IntegerField()
    content = serializers.CharField()
    publish = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    post_image_url = serializers.URLField()
    category = serializers.CharField()
    category_id = serializers.IntegerField()
    likes_count = serializers.IntegerField()
    dislikes_count = serializers.IntegerField()
    tags = serializers.ListSerializer(child=serializers.CharField())

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class NewPostDTOSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    post_image_url = serializers.URLField()
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    category_id = serializers.IntegerField()
    author_id = serializers.IntegerField()
    tags = serializers.ListSerializer(child=serializers.CharField())
    slug = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def run_validation(self, data):
        try:
            return super().run_validation(data)
        except ValidationError as exc:
            if "status" in exc.detail:
                exc.detail["status"] = self._custom_status_error_message()
            raise exc

    def _custom_status_error_message(self):
        available_choices = ", ".join([choice[0] for choice in STATUS_CHOICES])
        return f"Invalid status. Available choices are: {available_choices}."

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class PartialPostDTOSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    content = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    post_image_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False, allow_null=True)
    category_id = serializers.IntegerField(required=False, allow_null=True)
    tags = serializers.ListSerializer(child=serializers.CharField(), required=False, allow_null=True)
    slug = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def run_validation(self, data):
        try:
            return super().run_validation(data)
        except ValidationError as exc:
            if "status" in exc.detail:
                exc.detail["status"] = self._custom_status_error_message()
            raise exc

    def _custom_status_error_message(self):
        available_choices = ", ".join([choice[0] for choice in STATUS_CHOICES])
        return f"Invalid status. Available choices are: {available_choices}."

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class CommentDTOSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    body = serializers.CharField()
    post_id = serializers.IntegerField()
    author = serializers.CharField()
    author_id = serializers.IntegerField()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')


class NewCommentDTOSerializer(serializers.Serializer):
    body = serializers.CharField()
    post_id = serializers.IntegerField()
    author_id = serializers.IntegerField()

    def create(self, validated_data):
        raise NotImplementedError('Method not implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('Method not implemented')
