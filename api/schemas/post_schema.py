from drf_yasg import openapi

post_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Post ID"),
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Post title"),
        "slug": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, description="Post slug"),
        "author": openapi.Schema(type=openapi.TYPE_STRING, description="Author name"),
        "author_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Author ID"),
        "content": openapi.Schema(type=openapi.TYPE_STRING, description="Post content"),
        "publish": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Publish date"),
        "post_image_url": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                         description="Post image URL"),
        "category": openapi.Schema(type=openapi.TYPE_STRING, description="Category name"),
        "category_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Category ID"),
        "likes_count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of likes"),
        "dislikes_count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of dislikes"),
        "tags": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING),
                               description="List of tags"),
    },
)

posts_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "posts": openapi.Schema(type=openapi.TYPE_ARRAY, items=post_schema),
        "pages": openapi.Schema(type=openapi.TYPE_INTEGER, description="Total posts pages"),
        "current_page": openapi.Schema(type=openapi.TYPE_INTEGER, description="Current page"),
        "prev_page": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Has previously page"),
        "next_page": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Has next page")
    },
)

new_post_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Post title"),
        "content": openapi.Schema(type=openapi.TYPE_STRING, description="Post content"),
        "post_image_url": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                         description="Post image URL"),
        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Post status ('draft' or 'published')"),
        "category_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Category ID"),
        "tags": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="List of tags"),
        "slug": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG,
                               description="Post slug (optional)"),
    },
    required=["title", "content", "post_image_url", "status", "category_id"],
)

created_post_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "post": post_schema,
    },
)

partial_post_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Post title"),
        "content": openapi.Schema(type=openapi.TYPE_STRING, description="Post content"),
        "post_image_url": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                         description="Post image URL"),
        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Post status ('draft' or 'published')"),
        "category_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Category ID"),
        "tags": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING),
                               description="List of tags"),
        "slug": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG,
                               description="Post slug (optional)"),
    },
    required=[]
)
