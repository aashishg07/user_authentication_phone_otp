from rest_framework import viewsets, status
from .serializers import UserSerializer
from .models import User
import datetime
import random
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from .utils import send_otp


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["PATCH"])

    def verify_otp(self, request, pk=None):
        instance = self.get_object()

        if(not instance.is_active and instance.otp == request.data.get("otp") and instance.otp_expiry and timezone.now() < instance.otp_expiry):
            instance.is_active = True
            instance.otp_expiry = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.otp_max_out = None
            instance.save()
            return Response("Successfully verified the user.", status=status.HTTP_201_CREATED)
        return Response("User already exists or OTP didn't match.", status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=True, methods=["PATCH"])

    def regenerate_otp(self, request, pk=None):
        instance = self.get_object()

        if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_max_out:
            return Response("Max OTP try reached. Try after sometime.", status=status.HTTP_400_BAD_REQUEST)
        
        otp = random.randint(100000, 999999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=5)
        max_otp_try = int(instance.max_otp_try) - 1

        instance.otp = otp
        instance.otp_expiry = otp_expiry
        instance.max_otp_try = max_otp_try


        if max_otp_try == 0:
            instance.max_otp_try = timezone.now() + datetime.timedelta(minutes=10)
        elif max_otp_try == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY
        else:
            instance.otp_max_out = None
            instance.max_otp_try = max_otp_try
        instance.save()
        send_otp(instance.phone, otp)
        return Response("OTP re-generated successfully!", status=status.HTTP_200_OK)
