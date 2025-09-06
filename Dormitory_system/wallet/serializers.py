from rest_framework import serializers

class IncreaseBalance(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=10,decimal_places=2)

    def validate_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("Balance cannot be negative")
        return value