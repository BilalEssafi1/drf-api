from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.middleware.csrf import rotate_token
from .utils import clear_auth_cookies
from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)


@api_view()
def root_route(request):
    """
    Root route view
    Returns welcome message for API
    """
    return Response({
        "message": "Welcome to my drf API!"
    })


@api_view(['POST'])
def logout_route(request):
    """
    Custom logout view using unified cookie clearing
    """
    response = Response()
    response = clear_auth_cookies(response)
    rotate_token(request)
    return response
