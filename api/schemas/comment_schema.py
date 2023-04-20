from drf_yasg import openapi

comment_dto_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Comment ID"),
        "body": openapi.Schema(type=openapi.TYPE_STRING, description="Comment message"),
        "post_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Post ID"),
        "author": openapi.Schema(type=openapi.TYPE_STRING, description="Author username"),
        "author_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Author ID"),
        "created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                  description="Comment created timestamp"),
        "updated": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                  description="Comment updated timestamp"),
        "likes": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of likes"),
        "dislikes": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of dislikes"),
    }
)

comments_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "post_comments": openapi.Schema(type=openapi.TYPE_ARRAY, items=comment_dto_schema,
                                        description="List of post comments")
    }
)

new_comment_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "body": openapi.Schema(type=openapi.TYPE_STRING, description="Comment message"),
    }
)
