from rest_framework.decorators import api_view
from rest_framework.response import Response
from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)


@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to my drf API!"
    })

# dj-rest-auth logout view fix
@api_view(['POST'])
def logout_route(request):
    """
    Custom logout route to ensure cookies are explicitly deleted.
    """
    response = Response({"message": "Successfully logged out"})
    response.delete_cookie(
        key=JWT_AUTH_COOKIE,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.delete_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response