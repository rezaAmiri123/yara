from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import Profile, EmailVerification, User
from users.services import send_email_token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number', 'password',)

    def create(self, validated_data):
        instance = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number']
        )
        email_verification = EmailVerification.objects.create(user=instance)
        send_email_token(email=validated_data['email'], token=email_verification.verification_code)
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number', 'password', 'avatar')

    def validate_password(self, password):
        return make_password(password)

    def update(self, instance, validated_data):
        old_email = instance.email
        instance = super().update(instance, validated_data)
        if validated_data.get('email') and not old_email == validated_data.get('email'):
            EmailVerification.objects.filter(user__email=old_email).delete()
            email_verification = EmailVerification.objects.create(user=instance)
            send_email_token(email=validated_data['email'], token=email_verification.verification_code)

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    email = serializers.CharField(source='user.email')
    phone_number = serializers.CharField(source='user.phone_number')
    avatar = serializers.CharField(source='user.avatar')

    class Meta:
        model = Profile
        fields = ('city', 'company_name', 'address', 'time_zone', 'logo', 'full_name',
                  'email', 'phone_number', 'avatar')


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField()
