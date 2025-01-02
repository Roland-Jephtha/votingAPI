from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .apis import UserRegisterView,ProfileDetailsView,MyTokenObtainPairView,get_user_interest, RequestOTPView, VerifyOTPView, ChangePasswordView, LogoutAPIView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    # path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # profile
    path('profile/', ProfileDetailsView.as_view(), name="profiledetails"),
    # path('interests/', get_user_interest, name="interests"),
    path('logout/', LogoutAPIView.as_view(), name='logout'),


    path('request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),


]
