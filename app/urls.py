from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from app.views.account import AccountViewSet
from app.views.operation import OperationViewSet
from app.views.register import RegisterView

router = routers.DefaultRouter()
router.register('account', AccountViewSet, basename='account')
router.register('operation', OperationViewSet, basename='operation')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/', include(router.urls)),
    path('api/v1/token/', obtain_auth_token, name='token'),
    path('api/v1/register/', RegisterView.as_view(), name='register'),

    # Schema & Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Auth browsable API
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)