from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions,generics
from .serializers import IncreaseBalance
from .models import Wallet
from transaction.models import transaction
# Create your views here.
class IncreaseBalanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IncreaseBalance
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['balance']
        try:
            wal = Wallet.objects.get(user=request.user)
            # create transaction
            obj = transaction.objects.create(
                amount=amount,
                user=request.user,
                wallet=wal,
                t_type='D',
                t_status='C',
                )
            obj.save()
            # increase balance in wallet
            wal.balance += amount
            wal.save()
            return Response({
                "message": f"Increased balance",
                "amount": amount,
                "balance": wal.balance,
            },status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({'message': 'Wallet does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except:
            obj = transaction.objects.create(
                amount=amount,
                user=request.user,
                wallet=wal,
                t_type='D',
                t_status='F',
            )
            obj.save()
            return Response({'message': 'increase balance failed'}, status=status.HTTP_200_OK)