from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import UserRegisterSerializse, ProfileSerializer, InterestSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Interest, OTP
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .serializers import  RequestOTPSerializer, VerifyOTPSerializer, ChangePasswordSerializer
from django.conf import settings
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view

from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class RequestOTPView(APIView):
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                otp_code = get_random_string(6, allowed_chars='0123456789')
                OTP.objects.create(user=user, otp_code=otp_code)

          


                 # Send email
                subject = "Your OTP code"
                email_from = settings.EMAIL_HOST_USER
                message = f'Your OTP code is {otp_code}'

                send_mail(subject, message, email_from, [email], fail_silently=False,)



                return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']

            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.filter(user=user, otp_code=otp_code, is_verified=False).first()
                if otp:
                    otp.is_verified = True
                    otp.save()
                    return Response({'message': 'OTP verified'}, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.filter(user=user, is_verified=True).first()
                if otp:
                    user.set_password(new_password)
                    user.save()
                    otp.delete()  # Optionally delete OTP after password change
                    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
                return Response({'error': 'OTP not verified'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

#     def validate(self, attrs):
#         # Convert email to lowercase before validation
#         attrs['email'] = attrs['email'].lower()
#         return super().validate(attrs)

#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         # Add more claims if necessary
#         # ...

#         return token









# class LogoutAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         operation_description="Log out the authenticated user",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
#             },
#             required=['refresh'],
#         ),
#         responses={
#             200: openapi.Response('Successfully logged out.'),
#             400: openapi.Response('Error'),
#         }
#     )
#     def post(self, request, *args, **kwargs):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             # Blacklist the access token
#             access_token = request.auth
#             if access_token:
#                 BlacklistedToken.objects.create(token=str(access_token))

#             return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)









# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer




class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializse

    def post(self, request):
        serializer = UserRegisterSerializse(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class ProfileDetailsView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get_object(self):
        return self.request.user
    




