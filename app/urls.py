from django.urls import path
from .views import FirmViewSet, ShareViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'firms', FirmViewSet)
router.register(r'shares', ShareViewSet)

urlpatterns = router.urls