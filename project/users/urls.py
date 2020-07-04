from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserViewSet, ProfileViewSet

app_name = 'users'

urlpatterns = [
    path('user/', UserViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        # 'patch': 'partial_update',
    })),
    path('user/enabled/', UserViewSet.as_view({
        'post': 'enabled',
    })),

    path('profile/', ProfileViewSet.as_view({
        'get': 'retrieve',
    })),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),

]