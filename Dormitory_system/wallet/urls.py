from django.urls import path
from .views import IncreaseBalanceAPIView,Balance
urlpatterns = [
    path('increasebalance/', IncreaseBalanceAPIView.as_view()),
    path('getbalance/', Balance.as_view()),
]
