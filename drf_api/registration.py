from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from django.middleware.csrf import rotate_token
from django.conf import settings
from rest_framework import status

JWT_AUTH_COOKIE = getattr(settings, 'JWT_AUTH_COOKIE', None)
JWT_AUTH_REFRESH_COOKIE = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
JWT_AUTH_SAMESITE = getattr(settings, 'JWT_AUTH_SAMESITE', 'None')
JWT_AUTH_SECURE = getattr(settings, 'JWT_AUTH_SECURE', True)

class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        response = Response(
            {'detail': 'Registered successfully', 'redirect': '/signin'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

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

        # Clear all auth cookies
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

        rotate_token(request)
        return response