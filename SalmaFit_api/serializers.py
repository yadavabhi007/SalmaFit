from rest_framework import serializers
from .models import CountryCode, Notifications, User, Products
# from django.contrib.auth import password_validation
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from SalmaFit_api.utils import Util
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = serializers.ImageField(required=False)
    # password2 = serializers.CharField(style={'input_type':'password'}, write_only=True, required=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'device_token', 'profile', 'password']
        extra_kwargs = {
            'password':{'write_only':True}, 'phone':{'required':False}, 'profile':{'required':False}
        }

    # def validate(self, attrs):
    #     password = attrs.get('password')
    #     password2 = attrs.get('password2')
    #     if password != password2:
    #         raise serializers.ValidationError("Password And Confirm Password Doesn't Match")
    #     return attrs

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']


class VerifyAccountSerializer(serializers.Serializer):
    verify_email_otp = serializers.IntegerField()
    class Meta:
        fields = ['verify_email_otp']

        
class UserPhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    class Meta:
        model = User
        fields = ['phone']


class PasswordResetSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['phone', 'password']


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    device_token = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['email', 'device_token', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'profile']



class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True, style={'input_type':'password'},)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True, style={'input_type':'password'},)
    # new_password2 = serializers.CharField(max_length=128, write_only=True, required=True, style={'input_type':'password'},)

    def validate_old_password(self, value):
        user = self.context.get('user')
        if not user.check_password(value):
            raise serializers.ValidationError(
                ('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        # if data['new_password'] != data['new_password2']:
        #     raise serializers.ValidationError({'new_password2': ("The passwords didn't match.")})
        # password_validation.validate_password(data['new_password'], self.context.get('user'))
        password = data.get('new_password')
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return data


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://127.0.0.1:8000/api/reset-password/'+uid+'/'+token
            print('Password Reset Link', link)
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    # password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            # password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            # if password != password2:
            #     raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


# class StoresSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stores
#         fields = '__all__'


class CountryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryCode
        fields = '__all__'


# class UserProductImagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProductImages
#         fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    # stores = StoresSerializer(many=True)
    class Meta:
        model = Products
        fields = ['id', 'status', 'barcode_number', 'title', 'عنوان', 'brand', 'نامتجاری', 'barcode_image', 'product_image', 'nutrition_facts_image', 'ingredients_image', 'review', 'مرور', 'last_update', 'created_at', 'updated_at']


# class AboutUsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AboutUs
#         fields = '__all__'


# class TermsAndConditionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TermsAndConditions
#         fields = '__all__'

        

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

