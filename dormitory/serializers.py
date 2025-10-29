from rest_framework import serializers
from .models import dormitory
class dormitory_name_serializer(serializers.Serializer):
    name = serializers.CharField()
    Gender = serializers.SerializerMethodField()

    def get_Gender(self, obj):
        return obj.get_Gender_display()