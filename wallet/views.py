import uuid

from drf_spectacular.utils import extend_schema,OpenApiResponse,OpenApiTypes,OpenApiRequest,OpenApiExample
from rest_framework.views import APIView
from rest_framework import status,permissions,generics
from rest_framework.response import Response

from .serializers import IncreaseBalance
from .models import Wallet
from allusers.models import CustomUser,D_Admin,Student
from transaction.models import Transaction
from allusers.permitions import StudentUser,AdminUser
from logs.models import Logs
# Create your views here.
class IncreaseBalanceAPIView(APIView):
    permission_classes = [StudentUser]
    serializer_class = IncreaseBalance
    @extend_schema(
        request=IncreaseBalance,
        responses={
            200:{
                "description": "Increase balance",
                "example": {
                    "message": "Increase balance",
                    "amount":1000,
                    "balance":3000
                }
            },
            400:{
                "description": "Bad request",
                "example": {
                    "message": "balance must be an integer",
                    "message2": "balance cannot be negative"
                }
            },
            404:{
                "description": "Not found",
                "example":{
                    "message":"wallet not found"
                }
            }
        }
    )
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
        lg = Logs.objects.create(
            owner=request.user,
            role=request.user.Role,
            action="payment",
            detail="pending for charge balance",
            value=amount,
        )
        lg.save()
        try:

            wal = Wallet.objects.get(student=stu)
            # increase balance in wallet
            wal.balance += amount
            wal.save()
            # change transaction status
            obj.t_status = 'C'
            obj.save()
            # update log
            lg.details="successfully increased balance"
            lg.save()
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
            # update log
            lg.details="Increased balance failed"
            lg.save()
            return Response({'message': 'increase balance failed'}, status=status.HTTP_200_OK)


class Balance(APIView):
    permission_classes = [StudentUser]
    @extend_schema(
        responses={
            200: {
                "description": "success",
                "example": {
                    "balance": 1000,
                }

            },
            404:{
                "description": "Wallet does not exist",
                "example":{
                    "message":"Wallet does not exist"
                }
            }
        }
    )
    def get(self,request):
        try:
            Stu = Student.objects.get(user=request.user)
            wal = Wallet.objects.get(student=Stu)
            return Response({"balance": wal.balance}, status=status.HTTP_200_OK)

        except Wallet.DoesNotExist:
            return Response({'message': 'Wallet does not exist'}, status=status.HTTP_404_NOT_FOUND)