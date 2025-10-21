from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import CustomUser,Student
from dormitory.models import dormitory
from room.models import Room

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
    email = serializers.EmailField(allow_blank=False)
    class Meta:
        model = CustomUser
        fields = ['email','phonenumber']

        def validate_phonenumber(self, value):
            if value in [None,""]:
                raise serializers.ValidationError("Invalid phone number")
            return value
        def validate_email(self, value):
            if value in [None,'']:
                raise serializers.ValidationError("Invalid email")
            return value

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

class ProfileSerializer(serializers.ModelSerializer):
    dor_name = serializers.SerializerMethodField()
    dor_blk = serializers.SerializerMethodField()
    room_num = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','Role','phonenumber','email','National_number','dor_name','dor_blk','room_num']

    def get_dor_name(self,obj):
        try:
            user = self.context['request'].user
            stu = Student.objects.get(user=user)
            room = stu.room
            dor = room.dormitory
            return dor.name
        except Student.DoesNotExist:
            return ''

    def get_dor_blk(self,obj):
        try:
            user = self.context['request'].user
            stu = Student.objects.get(user=user)
            room = stu.room
            return room.Block_number
        except Student.DoesNotExist:
            print("Student does not exist")
            return ''

    def get_room_num(self,obj):
        try:
            user = self.context['request'].user
            stu = Student.objects.get(user=user)
            room = stu.room
            return room.room_number
        except Student.DoesNotExist:
            return ''
