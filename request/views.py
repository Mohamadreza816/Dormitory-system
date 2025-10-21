from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import date
from django.utils import timezone
import pytz
from django.shortcuts import render
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound, MethodNotAllowed
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import Requests
from .serializers import RequestSerializer,RequestsupdateSerializer
from allusers.permitions import StudentUser,AdminUser
from room.models import Room
from dormitory.models import dormitory
from logs.models import Logs
from drf_spectacular.utils import extend_schema, OpenApiParameter
# Create your views here.

class RequestList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self):
        student = self.request.user.student
        if self.request.user.Role == 'Admin':
            queryset = Requests.objects.for_user(self.request.user)
            return queryset
        queryset = Requests.objects.filter(room=student.room)
        return queryset

# create student [only students]
class RequestCreate(generics.CreateAPIView):
    permission_classes = [StudentUser]
    serializer_class = RequestSerializer
    def perform_create(self, serializer):
        serializer.save()
        #create log
        lg = Logs.objects.create(
            owner=self.request.user,
            role="student",
            action="create request",
            detail="Request created successfully",
        )
        lg.save()

# delete request [only students]
class RequestDelete(generics.DestroyAPIView):
    permission_classes = [StudentUser]

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            req = Requests.objects.get(pk=pk)
        except Requests.DoesNotExist:
            raise NotFound({"error": "Request not found"})

        if req.student != self.request.user.student:
            raise PermissionDenied("Error: You are not allowed to delete this request")
        if req.status.lower() != "p":
            raise PermissionDenied("Error: Only pending requests can be deleted")
        return req

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        mes = f"request {instance.r_type} deleted"
        # create log
        lg = Logs.objects.create(
            owner=self.request.user,
            role="student",
            action="delete request",
            detail=mes,
            request=instance,
        )
        lg.save()
        self.perform_destroy(instance)
        return Response({"message": mes},status=status.HTTP_204_NO_CONTENT)


class RequestUpdate(generics.UpdateAPIView):
    permission_classes = [AdminUser]
    serializer_class = RequestsupdateSerializer
    queryset = Requests.objects.all()
    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # update time
        instance.updated_at = timezone.now()
        instance.save()
        # create log
        lg = Logs.objects.create(
            owner=self.request.user,
            role="admin",
            action="update request",
            detail="Request updated successfully",
            request=instance,
        )
        lg.save()
        return super().update(request, *args, **kwargs)

# filter requests based on time,people,dormitory and status
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="f_type",
            type=str,
            location=OpenApiParameter.PATH,
            description= "filter type: all, me, pending, accepted, rejected, roommates, week, month, semester, Dormitory name",
        )
    ],
    responses=RequestSerializer(many=True),
)
class RequestFilter(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self):
        dor_name = ['Ghadir','Dabagh']
        user = self.request.user
        if user.Role == "student":
            student = user.student
        req = Requests.objects.for_user(self.request.user)

        filter_type = self.kwargs.get('f_type')

        if filter_type == "all" or filter_type == "me":
            return req
        elif filter_type == "pending":
            req = req.filter(status="P")

        elif filter_type == "accepted":
            req = req.filter(status="A")

        elif filter_type == "rejected":
            req = req.filter(status="R")

        elif filter_type == "roommates" and user.Role == "student":
            room = student.room
            req = Requests.objects.filter(room=room)

        elif filter_type == "roommates" and user.Role == "admin":
            ...

        elif filter_type == "week":
            one_week_ago = timezone.now() - timedelta(days=7)
            req = req.filter(created_at__gte=one_week_ago)

        elif filter_type == "month":
            one_month_ago = timezone.now() - relativedelta(months=1)
            req = req.filter(created_at__gte=one_month_ago)

        elif filter_type == "semester":
            today = timezone.localdate()
            year = today.year
            start = None
            end = None
            if date(year, 9, 23) <= today <= date(year + 1, 2, 19):
                if today.month >= 9:
                    start = date(year, 9, 23)
                    end = date(year + 1, 2, 19)
                else:
                    start = date(year - 1, 9, 23)
                    end = date(year, 2, 19)

            elif date(year, 2, 20) <= today <= date(year, 6, 21):
                start = date(year, 2, 20)
                end = date(year, 6, 21)

            elif date(year, 6, 22) <= today <= date(year, 9, 22):
                start = date(year, 6, 22)
                end = date(year, 9, 22)

            if start and end:
                req = req.filter(created_at__date__range=[start, end])
            else:
                req = req.none()

        elif (filter_type in dor_name) and user.Role == "admin":
            try:
                dor = dormitory.objects.get(name=filter_type)
                req = Requests.objects.filter(room__dormitory=dor)
            except dormitory.DoesNotExist:
                raise ValidationError({"error": "Dormitory not found"})
        else:
            raise ValidationError({"error": "Filter not found"})
        return req