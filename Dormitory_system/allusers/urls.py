from django.urls import path, include
from .views import UserLoginAPIView,create_link,changepassword_link,Editprofile
urlpatterns = [
    path('login/',UserLoginAPIView.as_view()),
    path('create_link/',create_link.as_view()),
    path('changepassword_link/',changepassword_link.as_view()),
    path('editprofile/',Editprofile.as_view()),
]