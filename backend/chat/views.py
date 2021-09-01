from rest_framework import viewsets, mixins

from chat.models import Room
from chat.serializers import RoomSerializer


class RoomViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
