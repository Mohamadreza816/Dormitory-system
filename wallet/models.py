from django.db import models
from allusers.models import Student
# Create your models here.
class Wallet(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)