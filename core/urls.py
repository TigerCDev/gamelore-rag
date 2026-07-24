from django.contrib import admin
from django.urls import path, include
from rag.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('games.urls')),
    path('api/v1/', include('rag.urls')),
    path('api/v1/health/', health_check),
]
