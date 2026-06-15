from rest_framework.routers import DefaultRouter
from .views import GameViewSet



router = DefaultRouter()
router.register(r'games', GameViewSet)

urlpatterns = router.urls
