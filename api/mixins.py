from rest_framework.mixins import (
    CreateModelMixin, RetrieveModelMixin, ListModelMixin
)
from rest_framework.viewsets import GenericViewSet


class CreateRetrieveListViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet
):
    pass
