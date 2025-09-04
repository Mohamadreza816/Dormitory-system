from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.template.defaultfilters import first
from room.models import Room

# for std number,personal number and national number
only_digits = RegexValidator(r'^\d+$', 'این فیلد فقط باید شامل عدد 10 رقمی باشد')


# Create your models here.
class CustomUser(AbstractUser):
    class Meta:
        db_table = "allusers_customuser"
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    PhoneNumber = models.CharField(max_length=10, null=False, blank=False)
    Role = models.CharField(max_length=10, blank=False, null=False)
    National_number = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید دقیقا ۱۰ رقم باشد')])
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    class Gender(models.TextChoices):
        MALE = 'M', 'Male',
        FEMALE = 'F', 'Female'
        UNSET = 'U', 'Unset'

    user_Gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.UNSET)
    def set_role(self):
        if self.is_admin:
            self.role = 'admin'
        else:
            self.role = 'student'

    def __str__(self):
        return f'{self.first_name}'


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,default=601)

    student_number = models.CharField(max_length=10, unique=True, blank=False, null=False
                                      , validators=[only_digits])
    study_field = models.CharField(max_length=30)

    def __str__(self):
        print(f"stuedent:{self.user.first_name} {self.user.last_name}")


class D_Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    level = models.IntegerField()
    personal_number = models.CharField(max_length=10, unique=True, blank=False, null=False
                                       , validators=[only_digits])

