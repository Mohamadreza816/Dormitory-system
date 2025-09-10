from rest_framework.views import APIView
import jwt
from .models import CustomUser,D_Admin,Student
from rest_framework.response import Response
from rest_framework import status, generics,permissions
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer,CreateLinkSerializer,UserEditProfileSerializer,ChangePasswordSerializer
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
            username = request.data.get('username')
            password = request.data.get('password')
            if not username or not password:
                return Response({'message': 'missing username or password'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=password)
            if user is not None:
                ref = RefreshToken.for_user(user)
                return Response({
                    'message': 'user login successfully',
                    'Role': user.Role,
                    'refresh': str(ref),
                    'access': str(ref.access_token)
                },status=status.HTTP_200_OK)
            else:
                return Response({'message': 'invalid credentials,user with this username and password dosen\'n exist'},status=status.HTTP_400_BAD_REQUEST)

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


class changepassword_link(APIView):
    serializer_class = ChangePasswordSerializer
    def put(self,request):
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
        serializer = self.serializer_class(instance=user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'password changed successfully'},status=status.HTTP_200_OK)

class Editprofile(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserEditProfileSerializer
    ALLOWED_FIELDS = {'email', 'phonenumber'}
    def update(self,request,*args,**kwargs):
        invalid = set(self.request.data.keys()) - self.ALLOWED_FIELDS
        if invalid:
            return Response(
                {"error": f"Invalid fields: {', '.join(invalid)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not request.data:
            return Response({"error": "missing data"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=request.user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'User profile updated',"new values":request.data},status=status.HTTP_200_OK)
