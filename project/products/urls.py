from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from products.views import BrandViewSet, ProductViewSet
from users.views import UserViewSet, ProfileViewSet

app_name = 'products'

router = DefaultRouter()
router.register('brands', BrandViewSet, basename='brands')
router.register('products', ProductViewSet, basename='products')
urlpatterns = [
    path('', include(router.urls))
]
