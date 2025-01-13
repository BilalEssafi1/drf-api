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


# Updated dj-rest-auth logout view fix
@api_view(['POST'])
def logout_route(request):
    """
    Custom logout view to clear authentication cookies and regenerate CSRF token.
    """
    response = Response({"message": "Logout successful"})
    
    # Clear authentication cookies
    response = Response({'message': 'Logged out successfully'})
    response.delete_cookie('my-app-auth', samesite='None', secure=True)
    response.delete_cookie('my-refresh-token', samesite='None', secure=True)
    response.delete_cookie('csrftoken', samesite='None', secure=True)
    
    return response
