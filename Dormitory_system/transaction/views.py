from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics,permissions
from .models import Transaction
from allusers.models import CustomUser,Student,D_Admin
from .serializers import TransactionListSerializer
from allusers.permitions import StudentUser
# Create your views here.

class transaction_list(generics.ListAPIView):
    permission_classes = [StudentUser]
    serializer_class = TransactionListSerializer

    def get_queryset(self):
        try:
            stu = Student.objects.get(user=self.request.user)
            return Transaction.objects.filter(student=stu).order_by('-created_at')
        except Student.DoesNotExist:
            return Response({"message":"Student dose not exist"},status=status.HTTP_404_NOT_FOUND)

