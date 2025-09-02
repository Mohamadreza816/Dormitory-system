from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
import uuid,random

study_field = [
    "Computer Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Unset"
]
admin_lev = [
    1,2,3
]
@receiver(post_save,sender=CustomUser)
def create_related_model(sender,instance,created,**kwargs):
    print("##############here in signal")
    if created:
        if instance.Role.lower() == "admin":
            D_Admin.objects.create(
                user=instance,
                level=random.choice(admin_lev),
                personal_number=str(uuid.uuid4().int)[:10]
            )

        elif instance.Role.lower() == "student":
            Student.objects.create(
                user=instance,
                student_number=str(uuid.uuid4().int)[:10],
                study_field=random.choice(study_field)
            )
