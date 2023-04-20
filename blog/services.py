import re
from typing import List, Optional, Dict, Tuple

from django.utils.text import slugify

from blog.dto import (
    CategoryDTO,
    NewCategoryDTO, PostDTO, NewPostDTO, PartialPostDTO, CommentDTO, NewCommentDTO, PaginatedResultDTO
)
from blog.exceptions import (
    CategoryAlreadyExistsError,
    CategoryDoesNotExistsError, PostDoesNotExistsError, PostCommentDoesNotExistsError
)
from blog.interfaces import (
    CategoryRepositoryInterface,
    CategoryServiceInterface, PostServiceInterface, PostRepositoryInterface, CommentRepositoryInterface,
    CommentServiceInterface
)


class SlugServiceMixin:
    def _validate_or_create_slug(self, value_to_slugify: str, user_slug: str | None) -> str:
        """Validate slug if exists or create if slug is None"""
        slug_pattern = re.compile(r'^[a-zA-Z0-9_-]+$')
        if user_slug is None or slug_pattern.match(user_slug) is None:
            slug = slugify(value_to_slugify)
            return slug
        return user_slug


class CategoryService(CategoryServiceInterface, SlugServiceMixin):
    """Service layer to work with categories domain logic"""
    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository

    def get_all_categories(self) -> List[CategoryDTO]:
        """Get all blog categories"""
        categories_dto = self.repository.get_all_categories()
        return categories_dto

    def get_category_by_id(self, category_id: int) -> CategoryDTO:
        """Get category by id or raise error"""
        category = self.repository.get_category_by_id(category_id)
        if category is None:
            raise CategoryDoesNotExistsError()
        return category

    def create_category(self, new_category_dto: NewCategoryDTO) -> CategoryDTO:
        """Create new category"""
        name = new_category_dto.name.title()
        slug = self._validate_or_create_slug(new_category_dto.name, new_category_dto.slug)

        existing_category = self.repository.category_exists(name, slug)
        if existing_category:
            raise CategoryAlreadyExistsError()

        category_dto = self.repository.create_category(name, slug)
        return category_dto

    def update_category(self, category_to_update: CategoryDTO) -> CategoryDTO:
        """Update exist category"""
        category = self.repository.get_category_by_id(category_to_update.id)
        if category is None:
            raise CategoryDoesNotExistsError()

        name = category_to_update.name.title()
        slug = self._validate_or_create_slug(name, category_to_update.slug)
        updated_category = self.repository.update_category(category.id, name, slug)
        return updated_category

    def delete_category_by_id(self, category_id: int) -> None:
        """Delete category by id"""
        category = self.repository.get_category_by_id(category_id)
        if category is None:
            raise CategoryDoesNotExistsError()
        self.repository.delete_category_by_id(category_id)


class PostService(PostServiceInterface, SlugServiceMixin):
    """Service layer to work with post domain logic"""
    def __init__(self, repository: PostRepositoryInterface):
        self.repository = repository

    def get_paginated_posts(self, page: int, per_page: int, specifications: Optional[List[Dict]] = None)\
            -> Tuple[List[PostDTO], PaginatedResultDTO]:
        """Get all blog posts"""
        posts_dto, paginated_result_dto = self.repository.get_paginated_posts(page, per_page, specifications)
        return posts_dto, paginated_result_dto

    def get_post_by_id(self, post_id: int) -> PostDTO:
        """Get post by id"""
        post = self.repository.get_post_by_id(post_id)
        if post is None:
            raise PostDoesNotExistsError()
        return post

    def delete_post_by_id(self, post_id: int) -> None:
        """Delete post by id"""
        post = self.repository.get_post_by_id(post_id)
        if post is None:
            raise PostDoesNotExistsError()
        self.repository.delete_post_by_id(post_id)

    def create_post(self, post_dto: NewPostDTO) -> PostDTO:
        """Create new post"""
        slug = self._validate_or_create_slug(post_dto.title, post_dto.slug)
        post_dto_data = post_dto._asdict()
        post_dto_data['slug'] = slug
        updated_post_dto = NewPostDTO(**post_dto_data)

        post_dto = self.repository.create_post(updated_post_dto)
        return post_dto

    def update_post(self, update_post_dto: NewPostDTO, post_id: int) -> PostDTO:
        """Update post"""
        post = self.repository.get_post_by_id(post_id)
        if post is None:
            raise PostDoesNotExistsError()

        slug = self._validate_or_create_slug(update_post_dto.title, update_post_dto.slug)
        update_post_dto = update_post_dto._replace(slug=slug)
        updated_post = self.repository.update_post(update_post_dto, post_id)
        return updated_post

    def update_partial_post(self, partial_post_dto: PartialPostDTO, post_id: int) -> PostDTO:
        """Update post partial"""
        post = self.repository.get_post_by_id(post_id)
        if post is None:
            raise PostDoesNotExistsError()

        post = self.repository.update_partial_post(partial_post_dto, post_id)
        return post


class CommentService(CommentServiceInterface):
    """Service layer to work with comment domain logic"""
    def __init__(self, repository: CommentRepositoryInterface):
        self.repository = repository

    def get_all_post_comments(self, post_id: int) -> List[CommentDTO]:
        """Get all comments by post_id"""
        post_comments = self.repository.get_all_post_comments(post_id)
        return post_comments

    def get_post_comment_by_id(self, post_id: int, comment_id: int) -> CommentDTO:
        """Get post comment by id or error"""
        post_comment = self.repository.get_post_comment_by_id(post_id, comment_id)
        if post_comment is None:
            raise PostCommentDoesNotExistsError()
        return post_comment

    def create_post_comment(self, new_comment: NewCommentDTO) -> CommentDTO:
        """Create post comment"""
        new_comment = self.repository.create_post_comment(new_comment.body,
                                                          new_comment.post_id,
                                                          new_comment.author_id)
        return new_comment

    def update_post_comment(self, update_comment: NewCommentDTO, old_comment: CommentDTO) -> CommentDTO:
        """Update post comment"""
        updated_comment = self.repository.update_post_comment(update_comment.body, old_comment.id)
        return updated_comment

    def delete_comment_by_id(self, comment_id: int) -> None:
        """Delete comment by id"""
        self.repository.delete_comment_by_id(comment_id)
