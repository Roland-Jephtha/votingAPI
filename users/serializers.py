from rest_framework import serializers
from .models import User,  OTP
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken










class CustomJWTAuthentication(JWTAuthentication):
    pass
    # def get_validated_token(self, raw_token):
    #     if BlacklistedToken.objects.filter(token=raw_token).exists():
    #         raise InvalidToken('Token is blacklisted')
    #     return super().get_validated_token(raw_token)




class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
    

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(max_length=128, write_only=True)

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['user', 'otp_code', 'created_at', 'is_verified']




class UserRegisterSerializse(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8, write_only=True)


    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password']


    def validate(self, attrs):
        email = attrs.get("email", "").lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email", ("email is already been used")}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)




class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField() 

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name",
                   "email",  "mobile", "country", "gender", 
                     "avatar",    "password" ]        
        
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance











# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         if not User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("User with this email does not exist.")
#         return value



