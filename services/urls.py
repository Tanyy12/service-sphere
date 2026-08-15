from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ServiceViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('services', ServiceViewSet)

urlpatterns = router.urls