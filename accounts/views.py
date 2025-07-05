from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer


User = get_user_model()


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_page(request):
    return render(request, 'login.html')


@csrf_exempt
def register_page(request):
    return render(request, 'register.html')

@csrf_exempt
def dashboard_page(request):
    return render(request, 'dashboard.html')


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerification(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "Token parameter missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # max_age in seconds; e.g., 3600 = 1 hour expiry
            data = signing.loads(token, salt='email-verification', max_age=3600)
        except SignatureExpired:
            return Response({"detail": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        # Create user with verified email and hashed password
        User = get_user_model()
        if User.objects.filter(email=data['email']).exists():
            return Response({"detail": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            email=data['email'],
            password=data['password'],
            is_active=True,
        )

        return Response({"detail": "Email verified and account created successfully."}, status=status.HTTP_201_CREATED)




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # This validates email + password and checks user.is_active
        data = super().validate(attrs)

        if not self.user.is_active:
            raise serializers.ValidationError('User account is not active. Please verify your email.')

        # Optionally add extra user info in response
        data['email'] = self.user.email
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer





class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)