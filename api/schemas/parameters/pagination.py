from drf_yasg import openapi

page_param = openapi.Parameter(
    "page",
    openapi.IN_QUERY,
    description="Page number",
    type=openapi.TYPE_INTEGER,
    default=1,
)

page_size_param = openapi.Parameter(
    "page_size",
    openapi.IN_QUERY,
    description="Number of items per page",
    type=openapi.TYPE_INTEGER,
    default=4,
)

pagination_parameters = [page_param, page_size_param]
