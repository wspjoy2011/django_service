from django.contrib import admin

from blog.models import (
    Category,
    Post,
    Comment,
    CommentLike,
    CommentDislike,
    PostLike,
    PostDislike,
    Follow
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    ordering = ('-status', '-publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('author', 'body')
    actions = ['deactivate_comments', 'activate_comments']

    def deactivate_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    search_fields = ('post__author', 'user__username')


@admin.register(PostDislike)
class PostDislikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    search_fields = ('post__author', 'user__username')


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user')
    search_fields = ('comment__author', 'user__username')


@admin.register(CommentDislike)
class CommentDislikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user')
    search_fields = ('comment__author', 'user__username')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_filter = ('follower', 'followed', 'created')
    list_display = ('id', 'follower_username', 'followed_username', 'created')

    def follower_username(self, obj):
        return obj.follower.username

    def followed_username(self, obj):
        return obj.followed.username

    follower_username.short_description = 'Follower'
    followed_username.short_description = 'Followed'
