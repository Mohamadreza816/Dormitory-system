from django.urls import path

from .views import RequestCreate,RequestList,RequestDelete,RequestUpdate,RequestFilter

urlpatterns = [
    path('create/', RequestCreate.as_view()),
    path('list/', RequestList.as_view()),
    path('delete/<int:pk>/', RequestDelete.as_view()),
    path('update/<int:pk>/', RequestUpdate.as_view()),
    path('filter/<str:f_type>/', RequestFilter.as_view()),
]