from django.conf import settings
from rest_framework import serializers
from .models import User
import random
from datetime import timedelta, datetime
from .utils import send_otp


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=settings.MIN_PASSWORD_LENGTH, 
                                      error_messages = {"min_length": f"Password must contain {settings.MIN_PASSWORD_LENGTH} characters."}
                                    )
    password2 = serializers.CharField(write_only=True, min_length=settings.MIN_PASSWORD_LENGTH, 
                                      error_messages = {"min_length": f"Password must contain {settings.MIN_PASSWORD_LENGTH} characters."}
                                      )
    

    class Meta:
        model = User
        fields = ['phone', 'email', 'password1', 'password2']

    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Password didn't match.")
        return data
    

    def create(self, validated_data):
        otp = random.randint(100000, 999999)
        otp_expiry = datetime.now() + timedelta(minutes=5)
        user = User(
            phone = validated_data["phone"],
            email = validated_data["email"],
            otp = otp,
            otp_expiry = otp_expiry,
            max_otp_try = settings.MAX_OTP_TRY
        )

        user.set_password(validated_data["password1"])
        user.save()
        send_otp(validated_data["phone"], otp)
        return user
