from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import root
from api.views import auth
from api.views import blog

app_name = 'api'


urlpatterns = [
    path('', root.ApiRootView.as_view(), name='api-root'),
    path('auth/register/', auth.ApiRegisterView.as_view(), name='api-register-user'),
    path('auth/activate/', auth.ApiActivateUserView.as_view(), name='api-activate-user'),
    path('auth/reactivate-token/', auth.ApiReactivateUserTokenView.as_view(), name='api-reactivate-token'),
    path('auth/password-token/', auth.ApiRequestPasswordResetView.as_view(), name='api-request-password-token'),
    path('auth/password-reset/', auth.ApiResetPasswordView.as_view(), name='api-password-reset'),
    path('jwt/token/', auth.JWTTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', auth.JWTTokenRefreshView.as_view(), name='token_refresh'),
    path('blog/categories/', blog.ApiCategoryListView.as_view(), name='api-blog-category-list'),
    path('blog/categories/<int:category_id>', blog.ApiCategoryDetailView.as_view(), name='api-blog-category-detail'),
    path('blog/posts/', blog.ApiPostListView.as_view(), name='api-blog-post-list'),
    path('blog/posts/<int:post_id>', blog.ApiPostDetailView.as_view(), name='api-blog-post-detail'),
    path('blog/posts/<int:post_id>/comments', blog.ApiPostCommentsListView.as_view(),
         name='api-blog-post-comments-list'),
    path('blog/posts/<int:post_id>/comments/<int:comment_id>', blog.ApiPostCommentsDetailView.as_view(),
         name='api-blog-post-comments-detail'),
]
