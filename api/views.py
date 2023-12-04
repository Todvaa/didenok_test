from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import ServiceNameSearchFilter
from api.mixins import CreateRetrieveListViewSet
from api.permissions import IsOwner
from api.serializers import AuthSerializer, PasswordManagerSerializer
from password_manager.models import User, PasswordManager


class MeView(GenericAPIView):
    """View for obtain information about user."""

    serializer_class = AuthSerializer

    def get(self, request):
        return Response(self.serializer_class(request.user).data)


class UserSignUpView(GenericAPIView):
    """View for User registration."""

    permission_classes = (AllowAny,)
    serializer_class = AuthSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        encrypted_password = make_password(password)
        try:
            user = User.objects.create(
                username=username,
                password=encrypted_password,
            )
        except IntegrityError:
            raise ValidationError({
                'error': 'This username is already in use'
            })

        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data)


class UserTokenObtainPairView(GenericAPIView):
    """View for User login."""

    permission_classes = (AllowAny,)
    serializer_class = AuthSerializer

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        try:
            user = User.objects.get(
                username=username,
            )
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')

        if not check_password(password, user.password):
            raise AuthenticationFailed('User not found', code='user_not_found')

        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data)


class PasswordManagerViewSet(CreateRetrieveListViewSet):
    """ViewSet for PasswordManager."""

    serializer_class = PasswordManagerSerializer
    permission_classes = (IsOwner & IsAuthenticated,)
    filter_backends = (ServiceNameSearchFilter,)
    lookup_field = 'service_name'

    def create(self, request, service_name) -> Response:
        """Creates and updates a password for the service."""

        password_manager_data = {
            'password': request.data.get('password'),
            'service_name': service_name,
        }
        password_manager = PasswordManager.objects.filter(
            service_name=service_name,
            user=request.user
        )
        if password_manager.exists():
            existing_manager = password_manager.first()
            serializer = self.get_serializer(
                existing_manager, data=password_manager_data
            )
        else:
            serializer = self.get_serializer(
                data=password_manager_data
            )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    def get_queryset(self):
        return PasswordManager.objects.filter(user=self.request.user)
