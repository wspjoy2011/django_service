from typing import NamedTuple, List, Optional
from datetime import datetime


class CategoryDTO(NamedTuple):
    id: int
    name: str
    slug: str


class NewCategoryDTO(NamedTuple):
    name: str
    slug: str | None = None


class PostDTO(NamedTuple):
    id: int
    title: str
    slug: str
    author: str
    author_id: int
    content: str
    publish: datetime
    post_image_url: str
    category: str
    category_id: int
    likes_count: int
    dislikes_count: int
    tags: List[str]


class NewPostDTO(NamedTuple):
    title: str
    content: str
    post_image_url: str
    status: str
    category_id: int
    tags: List[str]
    author_id: int
    slug: str | None = None


class PartialPostDTO(NamedTuple):
    title: Optional[str] = None
    content: Optional[str] = None
    post_image_url: Optional[str] = None
    status: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None


class CommentDTO(NamedTuple):
    id: int
    body: str
    post_id: int
    author: str
    author_id: int
    created: datetime
    updated: datetime
    likes: int
    dislikes: int


class NewCommentDTO(NamedTuple):
    body: str
    post_id: int
    author_id: int


class PaginatedResultDTO(NamedTuple):
    current_page: int
    total_pages: int
    has_previous: bool
    has_next: bool

