from rest_framework import serializers
from django.contrib.auth import get_user_model

from products.models import Brand, Product
from users.models import Profile, City, TimeZone

User = get_user_model()


class BrandCreateSerializer(serializers.ModelSerializer):
    country = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    time_zone = serializers.CharField(write_only=True)

    class Meta:
        model = Brand
        fields = ('email', 'phone_number', 'company_name', 'address', 'logo',
                  'country', 'state', 'city', 'time_zone')

    def normalize_validated_data(self, validated_data):
        country = validated_data.pop('country', None)
        state = validated_data.pop('state', None)
        city = validated_data.pop('city', None)
        time_zone = validated_data.pop('time_zone', None)
        city_obj, city_obj_created = City.objects.get_or_create(
            country=country,
            city=city,
            state=state
        )
        time_zone_obj, time_zone_obj_created = TimeZone.objects.get_or_create(name=time_zone)
        validated_data.update({
            'city': city_obj,
            'time_zone': time_zone_obj
        })

        return validated_data

    def create(self, validated_data):
        validated_data = self.normalize_validated_data(validated_data)
        instance = super().create(validated_data)

        return instance

    def update(self, instance, validated_data):
        validated_data = self.normalize_validated_data(validated_data)
        instance = super().update(instance, validated_data)

        return instance


class BrandSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='city.country')
    state = serializers.CharField(source='city.state')
    city = serializers.CharField(source='city.city')
    time_zone = serializers.CharField(source='time_zone.name')

    class Meta:
        model = Brand
        fields = ('id', 'email', 'phone_number', 'company_name', 'address', 'logo',
                  'country', 'state', 'city', 'time_zone')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'upc', 'logo', 'description', 'website', 'support_email', 'support_phone_number',
                  'cart_type', 'min_price', 'max_price', 'brand')
        read_only_fields = ('upc',)


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'logo', 'description', 'website', 'support_email', 'support_phone_number')
