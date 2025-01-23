from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.middleware.csrf import rotate_token
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
    Custom logout view
    Clears auth cookies and rotates CSRF token
    """
    response = Response()
    
    # Clear JWT auth cookies
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )

    # Clear session and CSRF cookies
    cookies_to_clear = ['csrftoken', 'sessionid', 'messages', 'my-app-auth', 'my-refresh-token']
    for cookie in cookies_to_clear:
        response.set_cookie(
            key=cookie,
            value='',
            httponly=True,
            expires='Thu, 01 Jan 1970 00:00:00 GMT',
            max_age=0,
            samesite='None',
            secure=True,
            path='/'
        )

    # Rotate CSRF token for security
    rotate_token(request)
    
    return response
