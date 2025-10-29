from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics,permissions
from rest_framework.views import APIView

from .models import dormitory
from .serializers import dormitory_name_serializer
from allusers.permitions import StudentUser,AdminUser
# Create your views here.
class dormitoryname(APIView):
    permission_classes = [AdminUser]
    serializer_class = dormitory_name_serializer
    def get(self,request):
        queryset = dormitory.objects.all()
        serializer = dormitory_name_serializer(queryset,many=True)
        return Response(serializer.data)