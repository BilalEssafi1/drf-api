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


# Enhanced dj-rest-auth logout view
@api_view(['POST'])
def logout_route(request):
    """
    Custom logout view to clear authentication cookies and additional cookies like sessionid and csrftoken.
    """
    try:
        response = Response({"message": "Logout successful"})

        # Clear JWT authentication cookies
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

        # Clear CSRF token cookie
        response.delete_cookie(
            key="csrftoken",
            samesite="None",
            secure=True
        )

        # Clear session ID cookie
        response.delete_cookie(
            key="sessionid",
            samesite="None",
            secure=True
        )

        return response

    except Exception as e:
        # Log the error for debugging
        print(f"Error during logout: {e}")
        return Response({"detail": "An error occurred during logout."}, status=500)
