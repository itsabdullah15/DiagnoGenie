from django.core.cache import cache
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import signing
from django.contrib.auth.hashers import make_password
from django.conf import settings
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email is already registered."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        # Hash the password before storing in token
        hashed_password = make_password(validated_data['password'])

        # Prepare data to sign
        data_to_sign = {
            'email': validated_data['email'],
            'password': hashed_password,
        }

        # Generate signed token with timestamp
        token = signing.dumps(data_to_sign, salt='email-verification')

        # Build verification URL
        verification_url = self.context['request'].build_absolute_uri(
            reverse('email-verify') + f"?token={token}"
        )
        subject = "Verify your email"
        message = f"Please verify your email by clicking this link: {verification_url}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [validated_data['email']]

        # For development, this prints email to console; in prod configure SMTP
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return {"detail": "Verification email sent. Please check your inbox."}

