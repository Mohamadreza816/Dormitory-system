from django.contrib.admin import action
from rest_framework import serializers
import uuid
from .models import Requests
from allusers.models import CustomUser,Student,D_Admin
from wallet.models import Wallet
from transaction.models import Transaction
from logs.models import Logs
class RequestSerializer(serializers.ModelSerializer):
    stu_firstname = serializers.SerializerMethodField()
    stu_lastname = serializers.SerializerMethodField()
    dor_name = serializers.SerializerMethodField()
    dor_blk = serializers.SerializerMethodField()
    room_num = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    class Meta:
        model = Requests
        fields = ['id','r_type','stu_firstname','stu_lastname','dor_name','dor_blk','room_num','created_date','description','status','is_priorty','comment']
        read_only_fields = ['id','stu_firstname','stu_lastname','dor_name','dor_blk','room_num','created_date','comment','status']

    def validate(self, data):
        if not data.get('r_type'):
            raise serializers.ValidationError({"r_type":"this field is required"})
        if not data.get('description'):
            raise serializers.ValidationError({"description":"this field is required"})
        return data

    def validate_is_priorty(self,data):
        cost = 3000
        obj = ...
        if data in [None,"",False]:
            return False
        if not isinstance(data, bool):
            raise serializers.ValidationError("is_priority must be true or false")
        user = self.context['request'].user
        obj = Transaction.objects.create(
            amount=cost,
            student=user.student,
            t_type='W',
            t_status='P',
            transaction_id=str(uuid.uuid4().int)[:8],
        )
        obj.save()
        # create log
        lg = Logs.objects.create(
            owner=user,
            role=user.Role,
            action="payment",
            detail="pending for priority",
            value=cost
        )
        lg.save()
        try:
            wal = Wallet.objects.get(student=user.student)
            if wal.balance < cost:
                obj.t_status = 'F'
                obj.save()
                # update log
                lg.detail="faild"
                lg.save()
                raise serializers.ValidationError({"is_priority":"this wallet balance is too low"})

            wal.balance = wal.balance - cost
            wal.save()
            obj.t_status = 'C'
            obj.save()
            #update log
            lg.detail="successfully paid"
            lg.save()
            return data
        except Wallet.DoesNotExist:
            raise serializers.ValidationError({"is_priority":"this user does not exist"})

        return data

    def get_stu_firstname(self,obj):
        return obj.student.user.first_name

    def get_stu_lastname(self,obj):
        return obj.student.user.last_name

    def get_dor_name(self,obj):
        stu = obj.student
        room = stu.room
        dor = room.dormitory
        return dor.name

    def get_dor_blk(self,obj):
        stu = obj.student
        room = stu.room
        return room.Block_number

    def get_room_num(self,obj):
        stu = obj.student
        room = stu.room
        return room.room_number


    def get_created_date(self,obj):
        return obj.created_at.date()

    def create(self,validated_data):
        user = self.context['request'].user
        try:
            stu = Student.objects.get(user=user)
            room = stu.room
            validated_data['student'] = stu
            validated_data['room'] = room
            return super().create(validated_data)
        except Student.DoesNotExist:
            return serializers.ValidationError({"student":"this student does not exist"})

class RequestsupdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = ['comment','status']
        extra_kwargs = {
            'comment': {'allow_blank': True}
        }
    def validate(self,data):
        if data.get('comment') == "":
            return data
        if not data.get('comment') and not data.get('status'):
            print(data)
            raise serializers.ValidationError({"comment":"this field is required","status":"this field is required"})
        return data

    def validate_status(self, data):
        if not data.upper() =="R" and not data.upper() =="A":
            raise serializers.ValidationError({"status":"status must be 'r(reject)' or 'a(accept)'"})
        return data

