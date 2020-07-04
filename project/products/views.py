from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from products.models import Brand, Product
from products.serializers import (
    BrandCreateSerializer,
    BrandSerializer,
    ProductUpdateSerializer,
    ProductSerializer,
)


class BrandViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    serializer_class = BrandCreateSerializer
    queryset = Brand.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        data = BrandSerializer(instance=instance).data

        return Response(data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        data = BrandSerializer(instance=instance).data

        return Response(data)

    def perform_update(self, serializer):
        return serializer.save()


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    filter_backends = (OrderingFilter, SearchFilter,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    ordering_fields = ('name', 'cart_type', 'id')
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'update':
            return ProductUpdateSerializer
        else:
            return ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ('list', 'retrieve'):
            queryset = queryset.filter(is_enable=True)
        return queryset

    @action(detail=True, url_path='enabled', methods=['POST'])
    def enabled(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_enable = not instance.is_enable
        instance.save()
        return Response(status=status.HTTP_200_OK)
