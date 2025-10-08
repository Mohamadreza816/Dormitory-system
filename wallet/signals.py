from django.db.models.signals import post_save
from django.dispatch import receiver
from wallet.models import Wallet
from allusers.models import Student

@receiver(post_save, sender=Student)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(student=instance, balance=0)