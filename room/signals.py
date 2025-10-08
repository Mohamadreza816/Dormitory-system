from django.db.models.signals import post_save
from django.dispatch import receiver
from room.models import Room
from dormitory.models import dormitory
import random

cap = [4, 6, 8]
block = [1, 2]

@receiver(post_save, sender=dormitory)
def create_room_model(sender, instance, created, **kwargs):
    for i in range(1, instance.rooms + 1):
        obj = Room.objects.create(
            dormitory=instance,
            room_number=i,
            capacity=random.choice(cap),
            Block_number=random.choice(block)
        )
        obj.save()
