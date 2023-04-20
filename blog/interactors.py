from typing import List, Optional, Dict, Tuple

from blog.dto import (
    CategoryDTO,
    NewCategoryDTO, PostDTO, NewPostDTO, PartialPostDTO, CommentDTO, NewCommentDTO, PaginatedResultDTO
)
from blog.interfaces import CategoryServiceInterface, PostServiceInterface, CommentServiceInterface


class CategoryInteractor:
    def __init__(self, category_service: CategoryServiceInterface):
        self.category_service = category_service

    def get_all_categories(self) -> List[CategoryDTO]:
        """Get all categories"""
        return self.category_service.get_all_categories()

    def get_category_by_id(self, category_id: int) -> CategoryDTO:
        """Get category by id"""
        return self.category_service.get_category_by_id(category_id)

    def create_category(self, new_category_dto: NewCategoryDTO) -> CategoryDTO:
        """Create new category"""
        return self.category_service.create_category(new_category_dto)

    def update_category(self, category_to_update: CategoryDTO) -> CategoryDTO:
        """Update category"""
        return self.category_service.update_category(category_to_update)

    def delete_category_by_id(self, category_id: int) -> None:
        """Delete category"""
        self.category_service.delete_category_by_id(category_id)


class PostInteractor:
    def __init__(self, post_service: PostServiceInterface, category_service: CategoryServiceInterface):
        self.post_service = post_service
        self.category_service = category_service

    def get_paginated_posts(self, page: int, per_page: int, conditions: Optional[List[Dict]] = None)\
            -> Tuple[List[PostDTO], PaginatedResultDTO]:
        """Get all posts"""
        return self.post_service.get_paginated_posts(page, per_page, conditions)

    def get_post_by_id(self, post_id: int) -> PostDTO:
        """Get post by id"""
        return self.post_service.get_post_by_id(post_id)

    def delete_post_by_id(self, post_id: int) -> None:
        """Delete post by id"""
        self.post_service.delete_post_by_id(post_id)

    def create_post(self, post_dto: NewPostDTO) -> PostDTO:
        """Create new post"""
        self.category_service.get_category_by_id(post_dto.category_id)
        return self.post_service.create_post(post_dto)

    def update_post(self, update_post_dto: NewPostDTO, post_id: int) -> PostDTO:
        """Update post"""
        self.category_service.get_category_by_id(update_post_dto.category_id)
        return self.post_service.update_post(update_post_dto, post_id)

    def update_partial_post(self, partial_post_dto: PartialPostDTO, post_id: int) -> PostDTO:
        """Update post partial"""
        if partial_post_dto.category_id is not None:
            self.category_service.get_category_by_id(partial_post_dto.category_id)
        return self.post_service.update_partial_post(partial_post_dto, post_id)


class CommentInteractor:
    def __init__(self, comment_service: CommentServiceInterface, post_service: PostServiceInterface):
        self.comment_service = comment_service
        self.post_service = post_service

    def get_all_post_comments(self, post_id: int) -> List[CommentDTO]:
        """Check if post exists. Get all comments by post_id"""
        self.post_service.get_post_by_id(post_id)
        post_comments = self.comment_service.get_all_post_comments(post_id)
        return post_comments

    def get_post_comment_by_id(self, post_id: int, comment_id: int) -> CommentDTO:
        """Check if post exists. Get comment by comment_id"""
        self.post_service.get_post_by_id(post_id)
        post_comment = self.comment_service.get_post_comment_by_id(post_id, comment_id)
        return post_comment

    def create_post_comment(self, new_comment: NewCommentDTO) -> CommentDTO:
        """Check if post exists and create post comment"""
        self.post_service.get_post_by_id(new_comment.post_id)
        new_comment = self.comment_service.create_post_comment(new_comment)
        return new_comment

    def update_post_comment(self, update_comment: NewCommentDTO, old_comment: CommentDTO) -> CommentDTO:
        """Update post comment"""
        updated_comment = self.comment_service.update_post_comment(update_comment, old_comment)
        return updated_comment

    def delete_comment_by_id(self, comment_id: int) -> None:
        """Check if post exists and delete comment"""
        self.comment_service.delete_comment_by_id(comment_id)

