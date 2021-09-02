from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RoomViewSet, MessageViewSet

router = DefaultRouter()
router.register("rooms", RoomViewSet, basename="rooms")
router.register("messages", MessageViewSet, basename="messages")


urlpatterns = [
    path("", include(router.urls)),
]
