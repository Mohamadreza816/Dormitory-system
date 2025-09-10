from django.db import models
from django.utils import timezone

from allusers.models import Student
# Create your models here.

class Transaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class Type(models.TextChoices):
        Deposit = "D","Deposit",
        Withdraw = "W","Withdraw",
        Unset = "U","Unset"

    t_type = models.CharField(max_length=1, choices=Type.choices, default=Type.Unset)
    class Status(models.TextChoices):
        Complete = 'C', 'Complete'
        Failed = 'F', 'Failed'
        Pending = 'P', 'Pending'
        UNSET = 'U', 'Unset'

    t_status = models.CharField(max_length=1, choices=Status.choices, default=Status.UNSET)
    created_at = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_id = models.CharField(max_length=8, unique=True, blank=False, null=False)