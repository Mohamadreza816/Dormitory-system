from django.db import models
from django.db.models import ForeignKey
from dormitory.models import dormitory

# Create your models here.
class Room(models.Model):
    dormitory = ForeignKey(dormitory, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    capacity = models.IntegerField(default=4)
    used = models.IntegerField(default=0)
    is_full = models.BooleanField(default=False)
    Block_number = models.IntegerField(default=0)
