from django.urls import path

from .views import (
    UserSignUpView, UserTokenObtainPairView,
    PasswordManagerViewSet, MeView
)

app_name = 'api'

urlpatterns = [
    path('auth/me/', MeView.as_view(), name='me'),
    path('auth/signup/', UserSignUpView.as_view(), name='sign_up'),
    path('auth/signin/', UserTokenObtainPairView.as_view(), name='get_token'),
    path(
        'password/<str:service_name>/', PasswordManagerViewSet.as_view(
            {'get': 'retrieve', 'post': 'create'}
        ), name='password_manager'
    ),
    path('password/', PasswordManagerViewSet.as_view({'get': 'list'}), name='password_list'),
]
