from django.urls import path
from .views import transaction_list

urlpatterns = [
    path('transaction_list/',transaction_list.as_view()),
]