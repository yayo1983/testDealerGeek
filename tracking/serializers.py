from rest_framework import serializers
from .models import Tracking


class TrackingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = '__all__'