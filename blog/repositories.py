from typing import List, Union, Any, Dict, Tuple, Optional

from annoying.functions import get_object_or_None
from django.db.models import Q, Count, QuerySet

from .dto import (
    CategoryDTO,
    PostDTO, NewPostDTO, PartialPostDTO, CommentDTO, PaginatedResultDTO
)
from .interfaces import (
    CategoryRepositoryInterface,
    PostRepositoryInterface, OrderSpecificationInterface, FilterSpecificationInterface, CommentRepositoryInterface,
    PaginationSpecificationInterface,
)
from .models import (
    Category,
    Post, Comment
)


class CategoryRepository(CategoryRepositoryInterface):
    """Category repository for DjangoORM"""

    def get_all_categories(self) -> List[CategoryDTO]:
        """Get all categories"""
        categories = Category.objects.all()
        return self._categories_dto(categories)

    def get_category_by_id(self, category_id: int) -> Union[CategoryDTO, None]:
        """Get category by id"""
        category = get_object_or_None(Category, pk=category_id)
        return self._category_dto(category) if category else None

    def create_category(self, name: str, slug: str) -> CategoryDTO:
        """Create new category"""
        category = Category.objects.create(
            name=name,
            slug=slug)
        category.save()
        return self._category_dto(category)

    def update_category(self, category_id: int, name: str, slug) -> CategoryDTO:
        """Update name and slug of category"""
        category = Category.objects.get(pk=category_id)
        category.name = name
        category.slug = slug
        category.save()
        return self._category_dto(category)

    def category_exists(self, name: str, slug: str) -> bool:
        """Return category or None by name and slug"""
        existing_category = Category.objects.filter(Q(name=name) | Q(slug=slug)).first()
        return existing_category is not None

    def delete_category_by_id(self, category_id: int) -> None:
        """Delete category by id"""
        category = Category.objects.get(pk=category_id)
        category.delete()

    def _category_dto(self, category: Category) -> CategoryDTO:
        """Return category as dto object"""
        category_dto = CategoryDTO(id=category.pk,
                                   name=category.name,
                                   slug=category.slug)
        return category_dto

    def _categories_dto(self, categories: List[Category]) -> List[CategoryDTO]:
        """Return categories as list of dto objects"""
        categories_dto = []
        for category in categories:
            category_dto = CategoryDTO(id=category.pk,
                                       name=category.name,
                                       slug=category.slug)
            categories_dto.append(category_dto)
        return categories_dto


class PostRepository(PostRepositoryInterface):
    """Post repository for DjangoORM"""
    def __init__(self, paginator: PaginationSpecificationInterface):
        self.pagination_spec = paginator

    def get_paginated_posts(self, page: int, per_page: int, specifications: Optional[List[Dict]] = None)\
            -> Tuple[List[PostDTO], PaginatedResultDTO]:
        """Get all posts"""
        query = Post.published.select_related('category', 'author') \
            .annotate(likes_count=Count('likes', distinct=True),
                      dislikes_count=Count('dislikes', distinct=True)) \
            .order_by("-publish")

        if specifications:
            query = self.apply_specifications(query, specifications)

        posts = query.all()
        paginated_posts, paginated_result_dto = self.pagination_spec.paginate(posts, page, per_page)
        posts_dto = self._posts_dto(paginated_posts)
        return posts_dto, paginated_result_dto

    def get_post_by_id(self, post_id: int) -> Union[PostDTO, None]:
        """Get post by id"""
        post = Post.published.filter(pk=post_id)\
            .select_related('category', 'author') \
            .annotate(likes_count=Count('likes', distinct=True),
                      dislikes_count=Count('dislikes', distinct=True)) \
            .first()
        return self._post_dto(post) if post else None

    def update_post(self, update_post_dto: NewPostDTO, post_id: int) -> PostDTO:
        """Update post"""
        post = Post.objects.get(pk=post_id)

        post.title = update_post_dto.title
        post.slug = update_post_dto.slug
        post.body = update_post_dto.content
        post.image_url = update_post_dto.post_image_url
        post.status = update_post_dto.status
        post.category_id = update_post_dto.category_id

        post.tags.clear()
        post.tags.add(*update_post_dto.tags)
        post.save()

        post.likes_count = post.likes.count()
        post.dislikes_count = post.dislikes.count()
        return self._post_dto(post)

    def update_partial_post(self, partial_post_dto: PartialPostDTO, post_id: int) -> PostDTO:
        """Partial post update"""
        post = Post.objects.get(pk=post_id)
        not_none_attributes = {key: value for key, value in partial_post_dto._asdict().items() if value is not None}

        for key, value in not_none_attributes.items():
            self._update_post_attribute(post, key, value)

        post.save()
        post.likes_count = post.likes.count()
        post.dislikes_count = post.dislikes.count()
        return self._post_dto(post)

    def delete_post_by_id(self, post_id: int) -> None:
        """Delete category by id"""
        post = Post.objects.get(pk=post_id)
        post.delete()

    def apply_specifications(self, query: QuerySet, conditions: List[Dict]) -> QuerySet:
        for condition in conditions:
            spec = condition["spec"]
            value = condition["value"]
            if isinstance(spec, FilterSpecificationInterface):
                query = query.filter(spec.build_query(value))
            elif isinstance(spec, OrderSpecificationInterface):
                query = spec.build_order(query, value)
        return query

    def create_post(self, post_dto: NewPostDTO) -> PostDTO:
        """Create new post"""
        post = Post.objects.create(
            title=post_dto.title,
            slug=post_dto.slug,
            author_id=post_dto.author_id,
            body=post_dto.content,
            image_url=post_dto.post_image_url,
            status=post_dto.status,
            category_id=post_dto.category_id)
        post.tags.add(*post_dto.tags)
        post.save()
        post.likes_count = 0
        post.dislikes_count = 0
        return self._post_dto(post)

    def _posts_dto(self, posts: List[Post]) -> List[PostDTO]:
        """Return posts as list of dto objects"""
        posts_dto = []
        for post in posts:
            post_dto = self._post_dto(post)
            posts_dto.append(post_dto)
        return posts_dto

    def _post_dto(self, post: Post) -> PostDTO:
        """Return post as dto object"""
        post_dto = PostDTO(id=post.pk,
                           title=post.title,
                           slug=post.slug,
                           author=post.author.username,
                           author_id=post.author.id,
                           content=post.body,
                           publish=post.publish,
                           post_image_url=post.image_url,
                           category=post.category.name,
                           category_id=post.category.pk,
                           likes_count=post.likes_count,
                           dislikes_count=post.dislikes_count,
                           tags=post.tags)
        return post_dto

    def _update_post_attribute(self, post: Post, key: str, value: Any) -> None:
        if key == 'content':
            post.body = value
        elif key == 'post_image_url':
            post.image_url = value
        elif key == 'tags':
            post.tags.clear()
            post.tags.add(*value)
        else:
            setattr(post, key, value)


class CommentRepository(CommentRepositoryInterface):
    """Comment repository for DjangoORM"""

    def get_all_post_comments(self, post_id: int) -> List[CommentDTO]:
        """Get all comments by post id"""
        comments = Comment.objects.filter(post_id=post_id, active=True) \
            .select_related('post', 'author') \
            .annotate(likes=Count("comment_likes", distinct=True),
                      dislikes=Count("comment_dislikes", distinct=True))\
            .order_by("-created")
        return self._post_comments_dto(comments)

    def get_post_comment_by_id(self, post_id, comment_id: int) -> Union[CommentDTO, None]:
        """Get post comment by id"""
        comment = Comment.objects.filter(id=comment_id, post_id=post_id, active=True)\
            .select_related('post', 'author') \
            .annotate(likes=Count("comment_likes", distinct=True),
                      dislikes=Count("comment_dislikes", distinct=True)) \
            .first()
        return self._post_comment_dto(comment) if comment else None

    def create_post_comment(self, body: str, post_id: int, author_id: int) -> CommentDTO:
        """Create post comment"""
        comment = Comment.objects.create(
            body=body,
            author_id=author_id,
            post_id=post_id)
        comment.save()
        comment.likes = 0
        comment.dislikes = 0
        return self._post_comment_dto(comment)

    def update_post_comment(self, body: str, comment_id: int) -> CommentDTO:
        """Update post comment"""
        comment = Comment.objects.get(id=comment_id, active=True)
        comment.body = body
        comment.save()
        return self.get_post_comment_by_id(comment.post.pk, comment.pk)

    def delete_comment_by_id(self, comment_id: int) -> None:
        """Delete category by id"""
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()

    def _post_comments_dto(self, comments: List[Comment]) -> List[CommentDTO]:
        """Return post comments as list of dto objects"""
        comments_dto = []
        for comment in comments:
            comment_dto = self._post_comment_dto(comment)
            comments_dto.append(comment_dto)
        return comments_dto

    def _post_comment_dto(self, comment: Comment) -> CommentDTO:
        """Return post comment as dto object"""
        comment_dto = CommentDTO(
            id=comment.pk,
            body=comment.body,
            post_id=comment.post.pk,
            author=comment.author.username,
            author_id=comment.author.id,
            created=comment.created,
            updated=comment.updated,
            likes=comment.likes,
            dislikes=comment.dislikes
        )
        return comment_dto
