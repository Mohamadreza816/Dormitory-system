from rest_framework.permissions import BasePermission
from .models import D_Admin,Student
# check for student user
class StudentUser(BasePermission):
    def has_permission(self, request, view):
        message = "This User is not a student"
        user = request.user
        if not user or not user.is_authenticated:
            return False

        try:
            stu = Student.objects.get(user=user)
            return True
        except Student.DoesNotExist:
            self.message = "This User is not a student"
            return False

# check for admin user
class AdminUser(BasePermission):
    def has_permission(self, request, view):
        message = "This User is not an admin"
        user = request.user
        if not user or not user.is_authenticated:
            return False
        try:
            admin = D_Admin.objects.get(user=user)
            return True
        except D_Admin.DoesNotExist:
            self.message = "This User dosen't exist"
            return False