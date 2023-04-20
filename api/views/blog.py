from typing import List, Dict, Tuple

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import JWTPermissionValidator
from api.schemas.category_schema import (
    category_schema,
    categories_response_schema,
    new_category_request_schema,
    created_category_response_schema
)
from api.schemas.comment_schema import (
    comments_response_schema,
    new_comment_schema,
    comment_dto_schema
)
from api.schemas.parameters.fillters import (
    author_filter_parameter,
    tags_filter_parameter,
    period_filter_parameter
)
from api.schemas.parameters.pagination import pagination_parameters
from api.schemas.post_schema import (
    posts_response_schema,
    new_post_request_schema,
    created_post_response_schema,
    post_schema,
    partial_post_request_schema
)
from blog.exceptions import (
    CategoryAlreadyExistsError,
    CategoryDoesNotExistsError,
    PostDoesNotExistsError,
    PostCommentDoesNotExistsError
)
from core.containers import (
    ProjectContainer as BlogContainer,
    FilterSpecificationContainer,
    OrderSpecificationContainer
)
from api.views.base import ApiBaseView
from api.serializers.blog import (
    CategoryDTOSerializer,
    NewCategoryDTOSerializer,
    PostDTOSerializer,
    NewPostDTOSerializer,
    PartialPostDTOSerializer,
    CommentDTOSerializer,
    NewCommentDTOSerializer
)
from blog.dto import (
    NewCategoryDTO,
    CategoryDTO,
    NewPostDTO,
    PartialPostDTO,
    NewCommentDTO
)


class ApiCategoryListView(APIView, ApiBaseView):
    """Get list of categories, add new category"""

    @swagger_auto_schema(
        operation_description="Get list of categories",
        responses={
            200: categories_response_schema,
            400: "Bad Request",
        },
        tags=["categories"],
        security=[],
    )
    def get(self, request):
        """Get list of categories"""
        category_interactor = BlogContainer.category_interactor()
        categories_dto = category_interactor.get_all_categories()

        categories_serializer = CategoryDTOSerializer(categories_dto, many=True)
        categories_serialized_data = categories_serializer.data
        return Response({
            'categories': categories_serialized_data},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create new category if category not exists",
        request_body=new_category_request_schema,
        responses={
            201: created_category_response_schema,
            400: "Bad Request",
            401: "Unauthorized",
            403: "Access Denied"
        },
        tags=["categories"],
        security=[{"Token Auth": []}],
    )
    def post(self, request):
        """Create new category if category not exists"""
        JWTPermissionValidator.is_superuser_or_raise(request)

        new_category_serializer = NewCategoryDTOSerializer(data=request.data)
        new_category_serializer_is_valid = new_category_serializer.is_valid()

        if not new_category_serializer_is_valid:
            return self._create_response_for_invalid_serializers(new_category_serializer)

        new_category_dto = NewCategoryDTO(**new_category_serializer.validated_data)
        category_interactor = BlogContainer.category_interactor()

        try:
            category_dto = category_interactor.create_category(new_category_dto)
        except CategoryAlreadyExistsError as exception:
            return self._create_response_for_exception(exception)

        category_serializer = CategoryDTOSerializer(category_dto)
        category_serialized_data = category_serializer.data
        return Response(
            {"new_category": category_serialized_data},
            status=status.HTTP_201_CREATED
        )


class ApiCategoryDetailView(APIView, ApiBaseView):
    """Get, update, delete category"""

    @swagger_auto_schema(
        operation_description="Get list of categories",
        responses={
            200: category_schema,
            400: "Bad Request",
            404: "Category not found"
        },
        tags=["categories"],
        security=[],
    )
    def get(self, request, category_id: int):
        """Get category detail by id"""
        category_interactor = BlogContainer.category_interactor()

        try:
            category_dto = category_interactor.get_category_by_id(category_id)
        except CategoryDoesNotExistsError as exception:
            return self._create_response_not_found(exception)

        category_serializer = CategoryDTOSerializer(category_dto)
        category_serialized_data = category_serializer.data
        return Response(
            {"category": category_serialized_data},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Update all fields in category",
        request_body=new_category_request_schema,
        responses={
            200: openapi.Response(description="Updated category", schema=category_schema),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Access Denied",
            404: "Category not found"
        },
        tags=["categories"],
        security=[{"Token Auth": []}],
    )
    def put(self, request, category_id: int):
        """Update all fields in category"""
        JWTPermissionValidator.is_superuser_or_raise(request)

        update_category_serializer = NewCategoryDTOSerializer(data=request.data)
        update_category_serializer_is_valid = update_category_serializer.is_valid()

        if not update_category_serializer_is_valid:
            return self._create_response_for_invalid_serializers(update_category_serializer)

        update_category_dto = NewCategoryDTO(**update_category_serializer.validated_data)
        category_dto = CategoryDTO(id=category_id,
                                   name=update_category_dto.name,
                                   slug=update_category_dto.slug)
        category_interactor = BlogContainer.category_interactor()

        try:
            updated_category_dto = category_interactor.update_category(category_dto)
        except CategoryDoesNotExistsError as exception:
            return self._create_response_not_found(exception)

        category_serializer = CategoryDTOSerializer(updated_category_dto)
        category_serialized_data = category_serializer.data
        return Response(
            {"category": category_serialized_data},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Delete category",
        responses={
            204: "Category deleted successfully",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Access Denied",
            404: "Category not found"
        },
        tags=["categories"],
        security=[{"Token Auth": []}],
    )
    def delete(self, request, category_id: int):
        """Delete category"""
        JWTPermissionValidator.is_superuser_or_raise(request)

        category_interactor = BlogContainer.category_interactor()
        try:
            category_interactor.delete_category_by_id(category_id)
        except CategoryDoesNotExistsError as exception:
            return self._create_response_not_found(exception)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiPostListView(APIView, ApiBaseView):
    """Get list of posts, add new post"""

    @swagger_auto_schema(
        operation_description="Get list of posts",
        responses={
            200: posts_response_schema,
            400: "Bad Request",
        },
        tags=["posts"],
        security=[],
        manual_parameters=[
            # Pagination parameters
            *pagination_parameters,
            # Filter parameters
            author_filter_parameter,
            tags_filter_parameter,
            period_filter_parameter
        ],
    )
    def get(self, request):
        """Get list of posts"""
        conditions = self.build_conditions_from_request(request)
        page, page_size = self._get_pagination_parameters(request)

        post_interactor = BlogContainer.post_interactor()
        posts_dto, paginated_result_dto = post_interactor.get_paginated_posts(page, page_size, conditions)

        posts_serializer = PostDTOSerializer(posts_dto, many=True)
        posts_serializer_data = posts_serializer.data
        return Response({
            'posts': posts_serializer_data,
            'pages': paginated_result_dto.total_pages,
            'current_page': paginated_result_dto.current_page,
            'prev_page': paginated_result_dto.has_previous,
            'next_page': paginated_result_dto.has_next},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new post",
        request_body=new_post_request_schema,
        responses={
            201: created_post_response_schema,
            400: "Bad Request",
            401: "Unauthorized",
        },
        tags=["posts"],
        security=[{"Token Auth": []}],
    )
    def post(self, request):
        """Create new post"""
        JWTPermissionValidator.validate_jwt_authentication_or_raise(request)

        user_id = request.user.id
        request_data = request.data.copy()
        request_data["author_id"] = user_id

        new_post_serializer = NewPostDTOSerializer(data=request_data)
        new_post_serializer_is_valid = new_post_serializer.is_valid()

        if not new_post_serializer_is_valid:
            return self._create_response_for_invalid_serializers(new_post_serializer)

        new_post_dto = NewPostDTO(**new_post_serializer.validated_data)
        post_interactor = BlogContainer.post_interactor()

        try:
            post_dto = post_interactor.create_post(new_post_dto)
        except CategoryDoesNotExistsError as exception:
            return self._create_response_not_found(exception)

        post_serializer = PostDTOSerializer(post_dto)
        post_serializer_data = post_serializer.data

        return Response({
            'post': post_serializer_data},
            status=status.HTTP_201_CREATED)

    def build_conditions_from_request(self, request) -> List[Dict]:
        filter_spec_container = FilterSpecificationContainer()
        filter_specifications = filter_spec_container.specifications_dict()

        order_spec_container = OrderSpecificationContainer()
        order_specifications = order_spec_container.specifications_dict()

        conditions = []

        author = request.GET.get("author")
        if author:
            author_spec = filter_specifications['author']
            conditions.append({"spec": author_spec, "value": author})

        tags = request.GET.get("tags")
        if tags:
            tag_list = tags.split(',')
            tag_spec = filter_specifications['tags']
            conditions.append({"spec": tag_spec, "value": tag_list})
            tags_count_spec = order_specifications["tags_count"]
            conditions.append({"spec": tags_count_spec, "value": tag_list})

        period = request.GET.get("period")
        if period:
            period_spec = filter_specifications['period']
            conditions.append({"spec": period_spec, "value": period})

        return conditions

    def _get_pagination_parameters(self, request) -> Tuple[int, int]:
        try:
            page = int(request.GET.get("page", 1))
            page_size = int(request.GET.get("page_size", 4))
        except ValueError:
            page = 1
            page_size = 4
        return page, page_size


class ApiPostDetailView(APIView, ApiBaseView):
    """Get, update, delete post"""

    @swagger_auto_schema(
        operation_description="Get list of posts",
        responses={
            200: post_schema,
            400: "Bad Request",
            404: "Post not found"
        },
        tags=["posts"],
        security=[],
    )
    def get(self, request, post_id: int):
        """Get post detail by id"""
        post_interactor = BlogContainer.post_interactor()

        try:
            post_dto = post_interactor.get_post_by_id(post_id)
        except PostDoesNotExistsError as exception:
            return self._create_response_not_found(exception)

        post_serializer = PostDTOSerializer(post_dto)
        post_serializer_data = post_serializer.data
        return Response(
            {"post": post_serializer_data},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update all fields in post",
        request_body=new_post_request_schema,
        responses={
            200: openapi.Response("Updated post", post_schema),
            400: "Invalid request data",
            401: "Unauthorized",
            403: "Access Denied",
            404: "Post not found",
        },
        tags=["posts"],
        security=[{"Token Auth": []}],
    )
    def put(self, request, post_id: int):
        """Update all fields in post"""
        JWTPermissionValidator.validate_jwt_authentication_or_raise(request)

        request_data = self._get_user_id_from_request(request)
        update_post_serializer = NewPostDTOSerializer(data=request_data)
        update_post_serializer_is_valid = update_post_serializer.is_valid()

        if not update_post_serializer_is_valid:
            return self._create_response_for_invalid_serializers(update_post_serializer)

        post_interactor = BlogContainer.post_interactor()

        try:
            post_dto = post_interactor.get_post_by_id(post_id)
        except PostDoesNotExistsError as exception:
            return self._create_response_not_found(exception)

        JWTPermissionValidator.is_superuser_or_object_author_or_raise(request, post_dto)
        update_post_dto = NewPostDTO(**update_post_serializer.validated_data)

        try:
            updated_post_dto = post_interactor.update_post(update_post_dto, post_id)
        except CategoryDoesNotExistsError as exception:
            return self._create_response_for_exception(exception)

        post_serializer = PostDTOSerializer(updated_post_dto)
        post_serializer_data = post_serializer.data
        return Response(
            {"post": post_serializer_data},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update some fields in post (partial update)",
        request_body=partial_post_request_schema,
        responses={
            200: openapi.Response("Updated post", post_schema),
            400: "Invalid request data",
            401: "Unauthorized",
            403: "Access Denied",
            404: "Post not found",
        },
        tags=["posts"],
        security=[{"Token Auth": []}],
    )
    def patch(self, request, post_id: int):
        JWTPermissionValidator.validate_jwt_authentication_or_raise(request)

        request_data = self._get_user_id_from_request(request)

        partial_post_serializer = PartialPostDTOSerializer(data=request_data)
        partial_post_serializer_is_valid = partial_post_serializer.is_valid()

        if not partial_post_serializer_is_valid:
            return self._create_response_for_invalid_serializers(partial_post_serializer)

        post_interactor = BlogContainer.post_interactor()

        try:
            post_dto = post_interactor.get_post_by_id(post_id)
        except PostDoesNotExistsError as exception:
            return self._create_response_not_found(exception)

        JWTPermissionValidator.is_superuser_or_object_author_or_raise(request, post_dto)
        partial_post_dto = PartialPostDTO(**partial_post_serializer.validated_data)

        try:
            updated_post_dto = post_interactor.update_partial_post(partial_post_dto, post_id)
        except CategoryDoesNotExistsError as exception:
            return self._create_response_not_found(exception)

        post_serializer = PostDTOSerializer(updated_post_dto)
        post_serializer_data = post_serializer.data
        return Response(
            {"post": post_serializer_data},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete post",
        responses={
            204: "Post deleted successfully",
            401: "Unauthorized",
            403: "Access Denied",
            404: "Post not found"
        },
        tags=["posts"],
        security=[{"Token Auth": []}],
    )
    def delete(self, request, post_id: int):
        """Delete post by id"""
        JWTPermissionValidator.validate_jwt_authentication_or_raise(request)
        post_interactor = BlogContainer.post_interactor()

        try:
            post_dto = post_interactor.get_post_by_id(post_id)
        except PostDoesNotExistsError as exception:
            return self._create_response_not_found(exception)

        JWTPermissionValidator.is_superuser_or_object_author_or_raise(request, post_dto)
        post_interactor.delete_post_by_id(post_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_user_id_from_request(self, request):
        user_id = request.user.id
        request_data = request.data.copy()
        request_data["author_id"] = user_id
        return request_data


class ApiPostCommentsListView(APIView, ApiBaseView):
    """Get list of post comments, add new comment to post"""

    @swagger_auto_schema(
        operation_description="Get list of post comments",
        responses={
            200: openapi.Response("Post comments", comments_response_schema),
            404: "Post not found",
        },
        tags=["post comments"],
        security=[]
    )
    def get(self, request, post_id: int):
        """Get list of post comments"""
        comment_interactor = BlogContainer.comment_interactor()
        try:
            post_comments_dto = comment_interactor.get_all_post_comments(post_id)
        except PostDoesNotExistsError as exception:
            return self._create_response_not_found(exception)

        post_comments_serializer = CommentDTOSerializer(post_comments_dto, many=True)
        post_comments_serializer_data = post_comments_serializer.data
        return Response({
            'post_comments': post_comments_serializer_data},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new post comment",
        request_body=new_comment_schema,
        responses={
            201: openapi.Response("New post comments", comment_dto_schema),
            400: "Bad Request",
            401: "Unauthorized",
            404: "Post not found",
        },
        tags=["post comments"],
        security=[{"Token Auth": []}],
    )
    def post(self, request, post_id: int):
        """Create new post comment"""
        JWTPermissionValidator.validate_jwt_authentication_or_raise(request)

        user_id = request.user.id
        request_data = request.data.copy()
        request_data["author_id"] = user_id
        request_data["post_id"] = post_id

        new_post_comment_serializer = NewCommentDTOSerializer(data=request_data)
        new_post_comment_serializer_is_valid = new_post_comment_serializer.is_valid()

        if not new_post_comment_serializer_is_valid:
            return self._create_response_for_invalid_serializers(new_post_comment_serializer)

        new_post_comment_dto = NewCommentDTO(**new_post_comment_serializer.validated_data)
        comment_interactor = BlogContainer.comment_interactor()

        try:
            post_comment_dto = comment_interactor.create_post_comment(new_post_comment_dto)
        except PostDoesNotExistsError as exception:
            return self._create_response_not_found(exception)

        post_comment_serializer = CommentDTOSerializer(post_comment_dto)
        post_comment_serializer_data = post_comment_serializer.data

        return Response({
            'comment': post_comment_serializer_data},
            status=status.HTTP_201_CREATED)


class ApiPostCommentsDetailView(APIView, ApiBaseView):
    """Get, update, delete post comment"""

    @swagger_auto_schema(
        operation_description="Post comment",
        responses={
            200: openapi.Response("Post comments", comment_dto_schema),
            404: "Post or comment not found",
        },
        tags=["post comments"],
        security=[],
    )
    def get(self, request, post_id: int, comment_id: int):
        """Get post comment"""
        comment_interactor = BlogContainer.comment_interactor()
        try:
            post_comment_dto = comment_interactor.get_post_comment_by_id(post_id, comment_id)
        except (PostDoesNotExistsError, PostCommentDoesNotExistsError) as exception:
            return self._create_response_not_found(exception)

        post_comment_serializer = CommentDTOSerializer(post_comment_dto)
        post_comment_serializer_data = post_comment_serializer.data
        return Response({
            'comment': post_comment_serializer_data},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update post comment",
        request_body=new_comment_schema,
        responses={
            200: openapi.Response("Updated post comments", comment_dto_schema),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Access Denied",
            404: "Post or comment not found",
        },
        tags=["post comments"],
        security=[{"Token Auth": []}],
    )
    def put(self, request, post_id: int, comment_id: int):
        """Update all field in post"""
        JWTPermissionValidator.validate_jwt_authentication_or_raise(request)

        user_id = request.user.id
        request_data = request.data.copy()
        request_data["author_id"] = user_id
        request_data["post_id"] = post_id

        update_post_comment_serializer = NewCommentDTOSerializer(data=request_data)
        update_post_comment_serializer_is_valid = update_post_comment_serializer.is_valid()

        if not update_post_comment_serializer_is_valid:
            return self._create_response_for_invalid_serializers(update_post_comment_serializer)

        update_post_comment_dto = NewCommentDTO(**update_post_comment_serializer.validated_data)
        comment_interactor = BlogContainer.comment_interactor()

        try:
            old_post_comment_dto = comment_interactor.get_post_comment_by_id(post_id, comment_id)
        except (PostDoesNotExistsError, PostCommentDoesNotExistsError) as exception:
            return self._create_response_not_found(exception)

        JWTPermissionValidator.is_superuser_or_object_author_or_raise(request, old_post_comment_dto)

        updated_post_comment_dto = comment_interactor.update_post_comment(update_post_comment_dto, old_post_comment_dto)

        updated_post_comment_serializer = CommentDTOSerializer(updated_post_comment_dto)
        updated_post_comment_serializer_data = updated_post_comment_serializer.data
        return Response({
            'comment': updated_post_comment_serializer_data},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete post comment",
        responses={
            204: "Post comment deleted successfully",
            401: "Unauthorized",
            403: "Access Denied",
            404: "Post or comment not found"
        },
        tags=["post comments"],
        security=[{"Token Auth": []}],
    )
    def delete(self, request, post_id: int, comment_id: int):
        """Delete post comment by id"""
        JWTPermissionValidator.validate_jwt_authentication_or_raise(request)
        comment_interactor = BlogContainer.comment_interactor()

        try:
            post_comment = comment_interactor.get_post_comment_by_id(post_id, comment_id)
        except (PostDoesNotExistsError, PostCommentDoesNotExistsError) as exception:
            return self._create_response_not_found(exception)

        JWTPermissionValidator.is_superuser_or_object_author_or_raise(request, post_comment)

        comment_interactor.delete_comment_by_id(comment_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
