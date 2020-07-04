from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from users.models import City, TimeZone


class CartType:
    MULTI_USE = 1
    DISPOSABLE = 2


def get_upc_number():
    return get_random_string(length=11, allowed_chars='0123456789')


class Brand(models.Model):
    email = models.EmailField(
        verbose_name=_('email'),
        help_text=_('email for this brand'),
        blank=True,
    )

    phone_number = models.CharField(
        verbose_name=_('phone'),
        help_text=_('the phone number of the user'),
        max_length=20,
        blank=True,
    )

    company_name = models.CharField(
        verbose_name=_('company name'),
        help_text=_('the company name for this brand'),
        max_length=255,
    )

    city = models.ForeignKey(
        verbose_name=_('city'),
        help_text=_('the city of the user'),
        to=City,
        on_delete=models.CASCADE,
        related_name='brands',
    )

    address = models.TextField(
        verbose_name=_('address'),
        help_text=_('the address for this brand'),
        max_length=255,
    )

    time_zone = models.ForeignKey(
        verbose_name=_('time zone'),
        help_text=_('time zone of the user'),
        to=TimeZone,
        on_delete=models.CASCADE,
        related_name='brands',
    )

    logo = models.CharField(
        verbose_name=_('logo'),
        help_text=_('the logo of this brand'),
        max_length=255,
        blank=True
    )

    activated = models.BooleanField(
        verbose_name=_('is active'),
        help_text=_('is this brand active'),
        default=False,
    )

    activator = models.IntegerField(
        verbose_name=_('activator'),
        help_text=_('activator of this brand'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.company_name


class Product(models.Model):
    CART_TYPE_CHOICES = (
        (CartType.MULTI_USE, _('Multi use')),
        (CartType.DISPOSABLE, _('Disposable')),
    )
    name = models.CharField(
        verbose_name=_('name'),
        help_text=_('the name for this product'),
        max_length=255,
    )

    upc = models.CharField(
        verbose_name=_('upc'),
        help_text=_('the upc for this product'),
        max_length=11,
        default=get_upc_number,
        unique=True
    )

    logo = models.CharField(
        verbose_name=_('logo'),
        help_text=_('the logo of this product'),
        max_length=255,
    )

    brand = models.ForeignKey(
        verbose_name=_('brand'),
        help_text=_('the brand of the product'),
        to=Brand,
        on_delete=models.CASCADE,
        related_name='products',
    )

    description = models.TextField(
        verbose_name=_('logo'),
        help_text=_('the logo of this product'),
        max_length=255,
        blank=True,
    )

    website = models.URLField(
        verbose_name=_('website'),
        help_text=_('the website of this product'),
        max_length=255,
    )

    support_email = models.EmailField(
        verbose_name=_('support email'),
        help_text=_('support email for this product'),

    )

    support_phone_number = models.CharField(
        verbose_name=_('support phone number'),
        help_text=_('the support phone number of the product'),
        max_length=20,
    )

    cart_type = models.PositiveSmallIntegerField(
        verbose_name=_('cart type'),
        help_text=_('the cart type for this product'),
        choices=CART_TYPE_CHOICES,
    )

    min_price = models.PositiveIntegerField(
        verbose_name=_('min price'),
        help_text=_('the min price of this product'),
    )

    max_price = models.PositiveIntegerField(
        verbose_name=_('max price'),
        help_text=_('the max price of this product'),
    )

    currency = models.CharField(
        verbose_name=_('currency'),
        help_text=_('the currency of the product'),
        max_length=20,
    )

    is_enable = models.BooleanField(
        verbose_name=_('is enable'),
        help_text=_('is this product enable'),
        default=False,
    )

    def __str__(self):
        return self.name



