from django.contrib.admin.views.decorators import staff_member_required
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Study project API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=[AllowAny],
)

staff_protected_schema_view = staff_member_required(schema_view.with_ui('swagger', cache_timeout=0))
