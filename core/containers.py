from dependency_injector import containers, providers

from accounts.repositories import UserRepository
from accounts.services import UserService
from accounts.interactors import RegisterInteractor
from blog.repositories import (
    CategoryRepository,
    PostRepository, CommentRepository
)
from blog.services import (
    CategoryService,
    PostService, CommentService
)
from blog.interactors import (
    CategoryInteractor,
    PostInteractor, CommentInteractor
)
from blog.specifications import AuthorSpecification, TagSpecification, PeriodSpecification, TagsCountSpecification, \
    PaginationSpecification
from email_services import RegisterEmailService


class OrderSpecificationContainer(containers.DeclarativeContainer):
    specifications_dict = providers.Dict({
        'tags_count': providers.Factory(TagsCountSpecification)
    })


class EmailServiceContainer(containers.DeclarativeContainer):
    registration_email_service = providers.Factory(RegisterEmailService)


class FilterSpecificationContainer(containers.DeclarativeContainer):
    specifications_dict = providers.Dict({
        'author': providers.Factory(AuthorSpecification),
        'tags': providers.Factory(TagSpecification),
        'period': providers.Factory(PeriodSpecification),
    })


class PaginateSpecificationsContainer(containers.DeclarativeContainer):
    paginator = providers.Factory(PaginationSpecification)


class RepositoryContainer(containers.DeclarativeContainer):
    user_repository = providers.Factory(UserRepository)
    category_repository = providers.Factory(CategoryRepository)
    post_repository = providers.Factory(
        PostRepository,
        paginator=PaginateSpecificationsContainer.paginator,
    )
    comment_repository = providers.Factory(CommentRepository)


class ServiceContainer(containers.DeclarativeContainer):
    user_service = providers.Factory(UserService, repository=RepositoryContainer.user_repository)
    category_service = providers.Factory(CategoryService, repository=RepositoryContainer.category_repository)
    post_service = providers.Factory(PostService, repository=RepositoryContainer.post_repository)
    comment_service = providers.Factory(CommentService, repository=RepositoryContainer.comment_repository)


class ProjectContainer(containers.DeclarativeContainer):
    register_interactor: providers.Provider[RegisterInteractor] = providers.Factory(
        RegisterInteractor,
        user_service=ServiceContainer.user_service,
        email_service=EmailServiceContainer.registration_email_service
    )
    category_interactor: providers.Provider[CategoryInteractor] = providers.Factory(
        CategoryInteractor,
        category_service=ServiceContainer.category_service
    )
    post_interactor: providers.Provider[PostInteractor] = providers.Factory(
        PostInteractor,
        post_service=ServiceContainer.post_service,
        category_service=ServiceContainer.category_service
    )
    comment_interactor: providers.Provider[CommentInteractor] = providers.Factory(
        CommentInteractor,
        comment_service=ServiceContainer.comment_service,
        post_service=ServiceContainer.post_service
    )

