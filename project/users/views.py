from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _
from users.models import Profile, EmailVerification, User
from users.serializers import (
    UserSerializer,
    UserUpdateSerializer,
    ProfileSerializer,
    EmailVerificationSerializer,
)
from users.services import send_email_token


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer

    @action(detail=False, url_path='enabled', methods=['POST'])
    def enabled(self, request, *args, **kwargs):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data.get('email'))
        if user.is_active:
            raise ValidationError({'user': _('user is activated')})
        instance = EmailVerification.objects.filter(
            user=user,
            verification_code=serializer.validated_data.get('verification_code')
        ).first()
        if not instance or instance.is_expired:
            if instance:
                instance.delete()
            email_verification = EmailVerification.objects.create(user=user)
            send_email_token(email=user.email, token=email_verification.verification_code)
            return Response(data={'verification_code': 'send code'}, status=status.HTTP_200_OK)
        instance.user.is_active = True
        instance.user.save()
        refresh = RefreshToken.for_user(instance.user)
        data = dict()
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return Response(data=data, status=status.HTTP_200_OK)


class ProfileViewSet(mixins.RetrieveModelMixin,
                     GenericViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        return self.request.user.profile
