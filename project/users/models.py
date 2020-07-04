import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from users.managers import UserManager


class UserType(object):
    BRAND = 1
    STORE = 2


def get_random_number():
    return get_random_string(length=4, allowed_chars='0123456789')


def expire_token_request_at():
    return timezone.now() + datetime.timedelta(days=1)


class User(AbstractBaseUser, PermissionsMixin):

    full_name = models.CharField(
        verbose_name=_('full name'),
        help_text=_('full name for this user'),
        max_length=255,
    )

    email = models.EmailField(
        verbose_name=_('email'),
        help_text=_('email for this user'),
        unique=True,
    )

    is_admin = models.BooleanField(
        verbose_name=_('is admin'),
        help_text=_('is this user admin?'),
        default=False,
    )

    email_is_verified = models.BooleanField(
        verbose_name=_('email is verified'),
        help_text=_('is this user email verified?'),
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name=_('is active'),
        help_text=_('is this user active?'),
        default=True,
    )

    activator = models.IntegerField(
        verbose_name=_('activator'),
        help_text=_('activator of this user'),
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        verbose_name=_('phone'),
        help_text=_('the phone number of the user'),
        max_length=20,
        blank=True,
    )

    avatar = models.CharField(
        verbose_name=_('avatar'),
        help_text=_('avatar for this user'),
        max_length=255,
        blank=True,
        default=''
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('full_name', 'phone_number')

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    objects = UserManager()


    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin


class City(models.Model):
    city = models.CharField(
        verbose_name=_('name'),
        help_text=_('the name of the city'),
        max_length=128,
    )
    country = models.CharField(
        verbose_name=_('country'),
        help_text=_('the country of the city'),
        max_length=128,
    )
    state = models.CharField(
        verbose_name=_('state'),
        help_text=_('the state of the city'),
        max_length=128,
    )

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class TimeZone(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        help_text=_('the name of the time zone'),
        max_length=128,
    )


class Profile(models.Model):
    user = models.OneToOneField(
        verbose_name=_('user'),
        help_text=_('the user of the profile'),
        to=User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    city = models.ForeignKey(
        verbose_name=_('city'),
        help_text=_('the city of the profile'),
        to=City,
        on_delete=models.CASCADE,
        related_name='profiles',
        null=True,
    )

    company_name = models.CharField(
        verbose_name=_('company name'),
        help_text=_('the company name for this user'),
        max_length=255,
    )

    address = models.TextField(
        verbose_name=_('address'),
        help_text=_('the address for this user'),
        max_length=255,
    )

    time_zone = models.ForeignKey(
        verbose_name=_('time zone'),
        help_text=_('time zone of the user'),
        to=TimeZone,
        on_delete=models.CASCADE,
        related_name='profiles',
        null=True,
    )

    logo = models.CharField(
        verbose_name=_('logo'),
        help_text=_('the logo of this user'),
        max_length=255,
        blank=True
    )

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


class EmailVerification(models.Model):
    user = models.ForeignKey(
        verbose_name=_('user'),
        help_text=_('the user of the email verification'),
        to=User,
        on_delete=models.CASCADE,
        related_name='email_verifications',
    )

    verification_code = models.CharField(
        verbose_name=_('verification code'),
        help_text=_('verification code '),
        max_length=255,
        default=get_random_number
    )

    expire_date = models.DateTimeField(
        default=expire_token_request_at
    )

    @property
    def is_expired(self):
        return self.expire_date < timezone.now()

    def __str__(self):
        return self.verification_code


class UserAccess(models.Model):
    CHOICES_USER_TYPE = (
        (UserType.BRAND, _('Brand')),
        (UserType.STORE, _('Store'))
    )

    user = models.ForeignKey(
        verbose_name=_('user'),
        help_text=_('the user of the this record'),
        to=User,
        on_delete=models.CASCADE,
        related_name='user_accesses',
    )

    user_type = models.PositiveSmallIntegerField(
        verbose_name=_('user type'),
        help_text=_('user type of this record'),
        choices=CHOICES_USER_TYPE
    )

    def __str__(self):
        return f'{self.user}:{self.user_type}'
