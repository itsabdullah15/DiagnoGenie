# project/urls.py or your app's urls.py

from django.urls import path
from .views import UserRegistrationView, EmailVerification, login_page, CustomTokenObtainPairView, register_page, dashboard_page, CurrentUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('verify-email/', EmailVerification.as_view(), name='email-verify'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    
    
    #FrontEnd Page
    path('login-page/', login_page, name='login-page'),
    path('register-page/', register_page, name='login-page'),
    path('', dashboard_page, name='dashboard-page'),
    
    
]