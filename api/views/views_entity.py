from rest_framework import generics

from api.models import Entity
from api.serializers import EntitySerializer


class EntityListApiView(generics.ListAPIView):
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()
