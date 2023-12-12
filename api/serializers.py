from rest_framework import serializers

from .models import Entity

# Create your serializers here.


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"
