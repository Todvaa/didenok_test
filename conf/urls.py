from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg.openapi import Info, Contact
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from conf import settings

schema_view = get_schema_view(
    Info(
        title='Passwords manager API',
        default_version='v1',
        description='API for passwords manager',
        contact=Contact(email='aa.varlamov1997@gmail.com'),
    ),
    public=True,
    permission_classes=[AllowAny,],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0
    ), name='schema-swagger-ui'),
    path('api/', include('api.urls', namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
