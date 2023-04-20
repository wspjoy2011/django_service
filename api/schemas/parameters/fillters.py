from drf_yasg import openapi

author_filter_parameter = openapi.Parameter(
                "author",
                openapi.IN_QUERY,
                description="Filter by author's username",
                type=openapi.TYPE_STRING,
            )

tags_filter_parameter = openapi.Parameter(
                "tags",
                openapi.IN_QUERY,
                description="Filter by tags (comma-separated list)",
                type=openapi.TYPE_STRING,
            )

period_filter_parameter = openapi.Parameter(
                "period",
                openapi.IN_QUERY,
                description="Filter by period (day, week, month)",
                type=openapi.TYPE_STRING,
            )
