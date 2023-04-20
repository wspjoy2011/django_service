from abc import ABCMeta, abstractmethod
from typing import List, Union, Optional, Dict, Tuple
from .dto import (
    CategoryDTO,
    NewCategoryDTO,
    PostDTO, NewPostDTO, PartialPostDTO, CommentDTO, NewCommentDTO, PaginatedResultDTO
)


class FilterSpecificationInterface(metaclass=ABCMeta):
    """Interface for FilterSpecifications"""

    @abstractmethod
    def build_query(self, *args):
        pass


class OrderSpecificationInterface(metaclass=ABCMeta):
    """Interface for OrderSpecifications"""

    @abstractmethod
    def build_order(self, *args):
        pass


class PaginationSpecificationInterface(metaclass=ABCMeta):
    """Paginate queryset"""

    @abstractmethod
    def paginate(self, *args) -> Tuple[List, PaginatedResultDTO]:
        pass


class CategoryRepositoryInterface(metaclass=ABCMeta):
    """Interface for CategoryRepository"""

    @abstractmethod
    def get_all_categories(self) -> List[CategoryDTO]:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Union[CategoryDTO, None]:
        pass

    @abstractmethod
    def update_category(self, category_id: int, name: str, slug) -> CategoryDTO:
        pass

    @abstractmethod
    def create_category(self, name: str, slug: str) -> CategoryDTO:
        pass

    @abstractmethod
    def category_exists(self, name: str, slug: str) -> bool:
        pass

    @abstractmethod
    def delete_category_by_id(self, category_id: int) -> None:
        pass


class PostRepositoryInterface(metaclass=ABCMeta):
    """Interface for PostRepository"""

    @abstractmethod
    def get_paginated_posts(self, page: int, per_page: int, specifications: Optional[List[Dict]] = None)\
            -> Tuple[List[PostDTO], PaginatedResultDTO]:
        pass

    @abstractmethod
    def get_post_by_id(self, post_id: int) -> Union[PostDTO, None]:
        pass

    @abstractmethod
    def create_post(self, post_dto: NewPostDTO) -> PostDTO:
        pass

    @abstractmethod
    def update_post(self, update_post_dto: NewPostDTO, post_id: int) -> PostDTO:
        pass

    @abstractmethod
    def update_partial_post(self, partial_post_dto: PartialPostDTO, post_id: int) -> PostDTO:
        pass

    @abstractmethod
    def delete_post_by_id(self, post_id: int) -> None:
        pass


class CommentRepositoryInterface(metaclass=ABCMeta):
    """Interface for CommentRepository"""

    @abstractmethod
    def get_all_post_comments(self, post_id: int) -> List[CommentDTO]:
        """Get all comments by post_id"""
        pass

    @abstractmethod
    def get_post_comment_by_id(self, post_id: int, comment_id: int) -> Union[CommentDTO, None]:
        """Get post comment by id"""
        pass

    @abstractmethod
    def create_post_comment(self, body: str, post_id: int, author_id: int) -> CommentDTO:
        """Create post comment"""
        pass

    def update_post_comment(self, body: str, comment_id: int) -> CommentDTO:
        """Update post comment"""
        pass

    @abstractmethod
    def delete_comment_by_id(self, comment_id: int) -> None:
        """Delete comment by id"""
        pass


class CategoryServiceInterface(metaclass=ABCMeta):
    """Interface for CategoryService"""

    @abstractmethod
    def get_all_categories(self) -> List[CategoryDTO]:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> CategoryDTO:
        pass

    @abstractmethod
    def create_category(self, new_category_dto: NewCategoryDTO) -> CategoryDTO:
        pass

    @abstractmethod
    def update_category(self, category_to_update: CategoryDTO) -> CategoryDTO:
        pass

    @abstractmethod
    def delete_category_by_id(self, category_id: int) -> None:
        pass


class PostServiceInterface(metaclass=ABCMeta):
    """Interface for PostService"""

    @abstractmethod
    def get_paginated_posts(self, page: int, per_page: int, specifications: Optional[List[Dict]] = None)\
            -> Tuple[List[PostDTO], PaginatedResultDTO]:
        pass

    @abstractmethod
    def get_post_by_id(self, post_id: int) -> Union[PostDTO, None]:
        pass

    @abstractmethod
    def create_post(self, post_dto: NewPostDTO) -> PostDTO:
        pass

    @abstractmethod
    def update_post(self, update_post_dto: NewPostDTO, post_id: int) -> PostDTO:
        pass

    @abstractmethod
    def update_partial_post(self, partial_post_dto: PartialPostDTO, post_id: int) -> PostDTO:
        pass

    @abstractmethod
    def delete_post_by_id(self, post_id: int) -> None:
        pass


class CommentServiceInterface(metaclass=ABCMeta):
    """Interface for CommentService"""

    @abstractmethod
    def get_all_post_comments(self, post_id: int) -> List[CommentDTO]:
        """Get all comments by post_id"""
        pass

    @abstractmethod
    def get_post_comment_by_id(self, post_id, comment_id: int) -> CommentDTO:
        """Get post comment by id"""
        pass

    @abstractmethod
    def create_post_comment(self, new_comment: NewCommentDTO) -> CommentDTO:
        """Create post comment"""
        pass

    @abstractmethod
    def update_post_comment(self, update_comment: NewCommentDTO, old_comment: CommentDTO) -> CommentDTO:
        """Update post comment"""
        pass

    @abstractmethod
    def delete_comment_by_id(self, comment_id: int) -> None:
        """Delete comment by id"""
        pass