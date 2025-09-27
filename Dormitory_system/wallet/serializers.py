import uuid
from rest_framework import serializers
from allusers.models import Student
from wallet.models import Wallet
from transaction.models import Transaction

class IncreaseBalance(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=10,decimal_places=2)

    def validate_balance(self, value):
        if value < 0:
            user = self.context['request'].user
            try:
                stu = Student.objects.get(user=user)
                obj = Transaction.objects.create(
                    amount=value,
                    student=stu,
                    t_type = 'D',
                    t_status = 'F',
                    transaction_id = str(uuid.uuid4())[:8],
                )
                obj.save()
                raise serializers.ValidationError("Balance cannot be negative")
            except Student.DoesNotExist:
                raise serializers.ValidationError("Student does not exist")
        if value > 100000:
            raise serializers.ValidationError("you can not increase your balance more than 100000")

        return value
