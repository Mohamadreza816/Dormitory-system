from rest_framework import serializers
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,write_only=True)
    password = serializers.CharField(required=True,write_only=True)

class CreateLinkSerializer(serializers.Serializer):
    email = serializers.CharField(required=True,write_only=True)