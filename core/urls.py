from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rag.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('games.urls')),
    path('api/v1/', include('rag.urls')),
    path('api/v1/health/', health_check),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
