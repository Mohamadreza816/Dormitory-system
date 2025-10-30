import random

from allusers.models import CustomUser
from ..signals import *
from wallet.signals import *


def run():

    first_names = [("علی","m"), ("سارا","f"), ("رضا","m"), ("مریم","f"), ("حسین","m"), ("فاطمه","f"), ("امیر","m"), ("نیلوفر","f"), ("مهدی","m"), ("آرزو","f")]
    last_names = ["احمدی", "حسینی", "کریمی", "مرادی", "جعفری", "رحیمی", "ابراهیمی", "شیرازی", "کاظمی", "فرهادی"]

    for i in range(1, 21):
        fname = random.choice(first_names)
        user_g = ...
        if fname[1] == 'm':
            user_g = "m"
        elif fname[1] == 'f':
            user_g = "f"

        lname = random.choice(last_names)
        national_number = str(1000000000 + i)
        phone_number = str(f'0912{random.randint(1000000, 9999999)}')

        if i % 2 == 0:
            role = "student"
            is_admin = False
            is_student = True
        else:
            role = "admin"
            is_admin = True
            is_student = False

        user = CustomUser.objects.create(
            username=f"user{i}",
            first_name=fname[0],
            last_name=lname,
            user_Gender=user_g,
            phonenumber=phone_number,
            Role=role,
            National_number=national_number,
            is_student=is_student,
            is_admin=is_admin,
        )
        user.set_password(national_number)
        user.save()
