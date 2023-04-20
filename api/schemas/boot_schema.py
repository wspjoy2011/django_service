from drf_yasg import openapi

api_root_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "endpoint": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "url": openapi.Schema(type=openapi.TYPE_STRING, description="Endpoint URL"),
                "info": openapi.Schema(type=openapi.TYPE_STRING, description="Endpoint info"),
            },
        ),
    },
)