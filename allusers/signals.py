from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
import uuid,random
from dormitory.models import dormitory
from room.models import Room
study_field = [
    "Computer Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
]
admin_lev = [
    1,2,3
]
@receiver(post_save,sender=CustomUser)
def create_related_model(sender,instance,created,**kwargs):
    if created:
        if instance.Role.lower() == "admin":
            obj = D_Admin.objects.create(
                user=instance,
                level=random.choice(admin_lev),
                personal_number=str(uuid.uuid4().int)[:10]
            )
            instance.username = obj.personal_number
            instance.save()
        elif instance.Role.lower() == "student" and instance.user_Gender == "m":
            temp = dormitory.objects.filter(Gender="M")
            empty_room = Room.objects.filter(is_full=False).order_by("-used")

            student_room = ...
            for room in empty_room:
                if room.used < room.capacity:
                    room.used += 1
                    student_room = room
                    if room.used == room.capacity:
                        room.is_full = True
                    room.save()
                    break

            obj = Student.objects.create(
                user=instance,
                room=student_room,
                student_number=str(uuid.uuid4().int)[:10],
                study_field=random.choice(study_field)
            )
            instance.username = obj.student_number
            instance.save()
        elif instance.Role.lower() == "student" and instance.user_Gender == "f":
            temp = dormitory.objects.filter(Gender="F")
            empty_room = Room.objects.filter(is_full=False).order_by("-used")

            student_room = ...
            for room in empty_room:
                if room.used < room.capacity:
                    room.used += 1
                    student_room = room
                    if room.used == room.capacity:
                        room.is_full = True
                    room.save()
                    break

            obj = Student.objects.create(
                user=instance,
                room=student_room,
                student_number=str(uuid.uuid4().int)[:10],
                study_field=random.choice(study_field)
            )
            instance.username = obj.student_number
            instance.save()