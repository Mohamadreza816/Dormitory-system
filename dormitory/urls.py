from django.urls import include, path
from .views import dormitoryname
urlpatterns = [
    path('name/',dormitoryname.as_view()),
]