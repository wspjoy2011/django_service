from drf_yasg import openapi

category_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Category ID"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Category name"),
        "slug": openapi.Schema(type=openapi.TYPE_STRING, description="Category slug"),
    },
)

categories_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "categories": openapi.Schema(type=openapi.TYPE_ARRAY, items=category_schema),
    },
)

new_category_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING,  description="Category name"),
        "slug": openapi.Schema(type=openapi.TYPE_STRING, description="Category slug"),
    },
    required=["name"]
)

created_category_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "new_category": category_schema,
    },
)
