from datetime import timedelta
from typing import List, Tuple

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.db.models import Q, QuerySet, Case, When, IntegerField, Sum

from blog.dto import PaginatedResultDTO
from blog.interfaces import (
    FilterSpecificationInterface,
    OrderSpecificationInterface,
    PaginationSpecificationInterface
)


class AuthorSpecification(FilterSpecificationInterface):
    """Filter objects by author using username of user model"""

    def build_query(self, author: str) -> Q:
        return Q(author__username__iexact=author)


class TagSpecification(FilterSpecificationInterface):
    """Filter objects by tags"""

    def build_query(self, tags: List[str]) -> Q:
        return Q(tags__name__in=tags)


class PeriodSpecification(FilterSpecificationInterface):
    """Filter objects by period (day, week, month)"""

    PERIODS = {
        'day': timedelta(days=1),
        'week': timedelta(weeks=1),
        'month': timedelta(days=30)
    }

    def build_query(self, period: str) -> Q:
        if period not in self.PERIODS:
            return Q()

        end_date = timezone.now()
        start_date = end_date - self.PERIODS[period]
        return Q(publish__range=(start_date, end_date))


class TagsCountSpecification(OrderSpecificationInterface):
    """Annotate queryset with count of tags and order by it in descending order."""

    def build_order(self, queryset: QuerySet, tags: List[str]) -> QuerySet:
        queryset = queryset.annotate(
            num_tags=Sum(
                Case(
                    When(tags__name__in=tags, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
        return queryset.order_by('-num_tags')


class PaginationSpecification(PaginationSpecificationInterface):
    """Paginate queryset"""

    def paginate(self, queryset: QuerySet, page: int, page_size: int) -> Tuple[List, PaginatedResultDTO]:
        paginator = Paginator(queryset, page_size)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        paginated_result_dto = PaginatedResultDTO(
            current_page=page_obj.number,
            total_pages=paginator.num_pages,
            has_previous=page_obj.has_previous(),
            has_next=page_obj.has_next()
        )
        return page_obj.object_list, paginated_result_dto
