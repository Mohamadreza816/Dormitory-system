from django.db import models

# Create your models here.
class dormitory(models.Model):
    name = models.CharField(max_length=100)
    class gender(models.TextChoices):
        male = 'M',"Male",
        female = 'F',"Female",
        unset = 'U',"Unset"

    rooms = models.IntegerField(default=0)
    Gender = models.CharField(max_length=1, choices=gender.choices, default=gender.unset)