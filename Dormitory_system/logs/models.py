from django.db import models
from allusers.models import CustomUser
from request.models import Requests
# Create your models here.
class Logs(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request = models.OneToOneField(Requests, on_delete=models.CASCADE,blank=True,null=True)
    role = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=30,blank=True, null=True)
    action = models.CharField(max_length=50)
    detail = models.TextField()

    def __str__(self):
        return f"{self.action} by {self.owner} at {self.created_at}"