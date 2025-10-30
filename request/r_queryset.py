from django.db import models

class RequestQuerySet(models.QuerySet):
    def for_user(self,user):
        if user.Role.lower() == "admin":
            return self.all().order_by("created_at")
        elif user.Role.lower() == "student":
            return self.filter(student=user.student).order_by("created_at")
        return self.none