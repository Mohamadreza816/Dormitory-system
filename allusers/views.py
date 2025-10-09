from rest_framework.views import APIView
import jwt
from .models import CustomUser,D_Admin,Student
from rest_framework.response import Response
from rest_framework import status, generics,permissions
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer, CreateLinkSerializer, UserEditProfileSerializer, ChangePasswordSerializer, \
    ProfileSerializer
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema,OpenApiResponse,OpenApiTypes,OpenApiRequest,OpenApiExample
from .generate_link import generate
from logs.models import Logs
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
            },
            401:{
                "description":"user not found",
                "example": {
                    "message": "invalid credentials,user with this username and password dosen\'n exist",
                }
            }
        }
    )
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username:
            return Response({'message': 'missing username'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'message': 'missing password'}, status=status.HTTP_400_BAD_REQUEST)
        # find user
        user = authenticate(username=username, password=password)
        # generate access and refresh token
        if user is not None:
            ref = RefreshToken.for_user(user)
            # create log
            lg = Logs.objects.create(
                owner=user,
                role="student",
                action="login",
                detail="User logged in successfully.",

            )
            lg.save()
            return Response({
                'message': 'user login successfully',
                'Role': user.Role,
                'refresh': str(ref),
                'access': str(ref.access_token)
            },status=status.HTTP_200_OK)
        else:
            return Response({'message': 'invalid credentials,user with this username and password dosen\'n exist'},status=status.HTTP_404_NOT_FOUND)

class logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=OpenApiRequest(
            {
                "type": "object",
                "properties": {
                    "refresh": {"type": "string"},
                },
                "required": ["refresh"],
            },
            examples=[
                OpenApiExample(
                    'Example',
                    value={"refresh": "your-refresh-token-here"},
                    request_only=True
                )
            ]
        ),
        responses={
            200 :{
                "example":{
                "message":"Successfully logged out"
            }

        },
            400:{
                "description": "Invalid credentials",
                "example":{
                    "message": "Invalid credentials",
                }
            }
        }
    )
    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
            if not token:
                return Response({'message': 'refresh is required'}, status=status.HTTP_400_BAD_REQUEST)
            # block refresh token
            token.blacklist()
            # create log
            lg = Logs.objects.create(
                owner=request.user,
                role= request.user.Role,
                action="logout",
                detail="Successfully logged out."
            )
            lg.save()
            return Response({"message": "Successfully logged out."}, status=200)
        except Exception as e:
            return Response({"error": 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class create_link(APIView):

    serializer_class = CreateLinkSerializer
    @extend_schema(
        request=CreateLinkSerializer,
        responses={
            200:{
                "description": "Link created successfully, send email",
                "example": {
                    "message": "email sent successfully",
                }
            },
            400:{
                "description": "Invalid credentials",
                "example": {
                    "message": "email is not correct",
                }
            }
        }
    )
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
            return Response({'message': 'email is not correct'},status=status.HTTP_400_BAD_REQUEST)


class changepassword_link(APIView):
    serializer_class = ChangePasswordSerializer

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200:{
                "description":"success",
                "example":{
                    "message":"Successfully changed password."
                }
            },
            400:{
                "description": "Invalid credentials",
                "example":{
                    "message": "Invalid credentials",
                }
            },
            404:{
                "description":"user not found",
                "example":{
                    "message": "user not found",
                }
            }

        }
    )
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
            return Response({"error": "user dosen\'t exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance=user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # create log
        lg = Logs.objects.create(
            owner=user,
            role=user.Role,
            action="change_password",
            detail="Successfully changed password."
        )
        lg.save()
        return Response({'message':'password changed successfully'},status=status.HTTP_200_OK)

class Editprofile(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserEditProfileSerializer
    ALLOWED_FIELDS = {'email', 'phonenumber'}

    @extend_schema(
        request=UserEditProfileSerializer,
        responses={
            200: {
                "description": "profile updated",
                "example": {
                    "message": "profile updated."
                }
            },
            400: OpenApiResponse({
                "description": "Invalid credentials",
                "example": {
                    "message": "missing data"
                }
            })
        }
    )
    def patch(self,request):
        return self.partial_update(request,partial=True)
    def update(self,request,*args,**kwargs):
        invalid = set(self.request.data.keys()) - self.ALLOWED_FIELDS
        if invalid:
            return Response(
                {"error": f"Invalid fields: {', '.join(invalid)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not request.data or None:
            return Response({"error": "missing data"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=request.user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # create log
        lg = Logs.objects.create(
            owner=request.user,
            role=request.user.Role,
            action="editprofile",
            detail="Successfully edited profile.",
            value=serializer.data
        )
        lg.save()
        return Response({'message': 'User profile updated',"new values":request.data},status=status.HTTP_200_OK)

class profile_detail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self,request,*args,**kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj,context={'request':request})
        return Response(serializer.data)

class RefreshAPIView(APIView):
    @extend_schema(
        responses={
            200: {
                "description": "new access token",
                "example": {
                    "message": "new access token generated.",
                    "access": "your-access-token-here"
                }
            },
            400: {
                "description": "Invalid credentials",
                "example": {
                    "message": "Invalid refresh token"
                }
            }
        }
    )
    def post(self,request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"error": "missing refresh token"}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return Response({'access_token': new_access_token},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=400)



class checklogin(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        responses={
            200 :{
            "example":{
                "message":"User logged in",
                "user":"username"
            }
            }
        }
    )
    def get(self, request):
        return Response({"message": "User logged in","user":request.user.username}, status=200)
