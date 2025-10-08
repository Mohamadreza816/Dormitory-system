from rest_framework import serializers
from .models import Transaction
from allusers.serializers import UserSerializer
class TransactionListSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id','student' ,'t_type','t_status','created_date', 'created_time', 'amount']

    def get_created_date(self,obj):
        return obj.created_at.date()
    def get_created_time(self,obj):
        return obj.created_at.time()