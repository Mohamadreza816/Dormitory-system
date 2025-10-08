from datetime import timezone

from django.db import models
from allusers.models import CustomUser,Student,D_Admin
from room.models import Room
from .r_queryset import RequestQuerySet
# Create your models here.
class Requests(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    class Status(models.TextChoices):
        rejected = "R","rejected"
        accepted = "A","accepted"
        pending = "P","pending"
        unsent = "U","unsent"

    status = models.CharField(max_length=1,choices=Status.choices, default=Status.pending)
    is_priorty = models.BooleanField(default=False)
    class Types(models.TextChoices):
        repairs = "R","repairs"
        cleaning = "C","cleaning"
        complaint = "CT","complaint"
        requiredequipment = "RE","requiredequipment"
        unset = "U","unset"

    r_type = models.CharField(max_length=2,choices=Types.choices, default=Types.unset)
    created_at = models.DateTimeField(auto_now_add=True)
    # admin fields
    updated_at = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=200,blank=True,null=True)

    objects = RequestQuerySet.as_manager()