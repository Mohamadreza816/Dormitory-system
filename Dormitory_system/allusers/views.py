from rest_framework.views import APIView
import jwt
from .models import CustomUser,D_Admin,Student
from rest_framework.response import Response
from rest_framework import status, generics
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from allusers.serializers import UserLoginSerializer,CreateLinkSerializer
from drf_spectacular.utils import extend_schema
from .generate_link import generate
# Create your views here.
class UserLoginAPIView(APIView):
    @extend_schema(
        request=UserLoginSerializer,
        responses={
            200: {
                "description": "user logged in successfully",
                "example": {
                    "message": "user logged in successfully.",
                }
            },
            400: {
                "description": "Invalid credentials",
                "example": {
                    "message": "Invalid credentials",
                }
            }
        }
    )
    def post(self,request):
        try:
            username = request.data['username']
            password = request.data['password']
            user = CustomUser.objects.get(National_number=password)
            # check user is stu or admin
            user_ = 'temp'
            if user.Role == 'admin':
                user_ = D_Admin.objects.get(personal_number=username)
            elif user.Role == 'student':
                user_ = Student.objects.get(student_number=username)
            else:
                return Response({'message':'role undefined'},status=status.HTTP_403_FORBIDDEN)

            if user_ is not None:
                ref = RefreshToken.for_user(user)
                return Response({
                    'message': 'user login successfully',
                    'Role': user.Role,
                    'refresh': str(ref),
                    'access': str(ref.access_token)
                },status=status.HTTP_200_OK)
            else:
                return Response({'message': 'invalid credentials,user with this username and password dosen\'n exist'},status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'message': 'user login failed,password is incorrect'},status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({'message': 'user login failed,username is incorrect'},status=status.HTTP_400_BAD_REQUEST)
        except D_Admin.DoesNotExist:
            return Response({'message': 'user login failed,username is incorrect'},status=status.HTTP_400_BAD_REQUEST)


class create_link(APIView):
    serializer_class = CreateLinkSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            tk = generate.generate_magic_link_token(user)
            generate.send_email(tk,user)
            return Response({'message':'Email send'},status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'email is wrong'},status=status.HTTP_400_BAD_REQUEST)


class login_link(APIView):
    def get(self,request):
        tk = request.GET.get('token')
        try:
            payload = jwt.decode(tk,settings.SECRET_KEY,algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"error": "Expired link"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        if payload.get("purpose") != "magic_link":
            return Response({"error": "Invalid token for purpose"}, status=status.HTTP_400_BAD_REQUEST)
        user = ...
        try:
            user = CustomUser.objects.get(id=payload['user_id'])
        except CustomUser.DoesNotExist:
            return Response({"error": "user dosen\'t exist"}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })