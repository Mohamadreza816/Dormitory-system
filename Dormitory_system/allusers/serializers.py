from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from allusers.models import CustomUser


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,write_only=True)
    password = serializers.CharField(required=True,write_only=True)

class CreateLinkSerializer(serializers.Serializer):
    email = serializers.CharField(required=True,write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name','Role']

class UserEditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','phonenumber']

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True,write_only=True)
    confirm_password = serializers.CharField(required=True,write_only=True)

    def validate(self,data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords must match')
        try:
            validate_password(data['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError(e.error_list)
        return data

    def update(self,instance,validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
