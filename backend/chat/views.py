from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins

from chat.models import Room, Message
from chat.serializers import RoomSerializer, MessageModelSerializer


class RoomViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MessageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("room__name",)
