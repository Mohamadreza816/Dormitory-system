import uuid
from dis import print_instructions

from adodbapi.ado_consts import adModeRead
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions,generics
from .serializers import IncreaseBalance
from .models import Wallet
from allusers.models import CustomUser,D_Admin,Student
from transaction.models import Transaction
from allusers.permitions import StudentUser,AdminUser
# Create your views here.
class IncreaseBalanceAPIView(APIView):
    permission_classes = [StudentUser]
    serializer_class = IncreaseBalance
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['balance']

        # create transaction with pending status
        t_id = str(uuid.uuid4().int)[:8]
        stu = Student.objects.get(user=request.user)
        obj = Transaction.objects.create(
            amount=amount,
            student=stu,
            t_type='D',
            t_status='P',
            transaction_id=t_id,
        )
        obj.save()

        try:

            wal = Wallet.objects.get(student=stu)
            # increase balance in wallet
            wal.balance += amount
            wal.save()
            # change transaction status
            obj.t_status = 'C'
            obj.save()
            return Response({
                "message": f"Increased balance",
                "amount": amount,
                "balance": wal.balance,
            },status=status.HTTP_200_OK)

        except Wallet.DoesNotExist:
            return Response({'message': 'Wallet does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except:
            obj.t_status = 'F'
            obj.save()
            return Response({'message': 'increase balance failed'}, status=status.HTTP_200_OK)


class Balance(APIView):
    permission_classes = [StudentUser]

    def get(self,request):
        try:
            Stu = Student.objects.get(user=request.user)
            wal = Wallet.objects.get(student=Stu)
            return Response({"balance": wal.balance}, status=status.HTTP_200_OK)

        except Wallet.DoesNotExist:
            return Response({'message': 'Wallet does not exist'}, status=status.HTTP_404_NOT_FOUND)