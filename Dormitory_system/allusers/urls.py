from django.urls import path, include
from .views import UserLoginAPIView,create_link,login_link
urlpatterns = [
    path('login/',UserLoginAPIView.as_view()),
    path('create_link/',create_link.as_view()),
    path('login_link/',login_link.as_view()),
]