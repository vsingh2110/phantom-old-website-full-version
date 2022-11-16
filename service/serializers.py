from rest_framework import serializers

from core.serializers import BaseModelSerializer
from .models import Service

class ServiceListSerializer(BaseModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

