from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from django.middleware.csrf import rotate_token
from django.conf import settings

class CustomRegisterView(RegisterView):
    def perform_create(self, serializer):
        user = super().perform_create(serializer)
        response = Response({'detail': 'Registered successfully'})
        
        # Clear JWT auth cookies
        response.set_cookie(
            key=settings.JWT_AUTH_COOKIE,
            value='',
            httponly=True,
            expires='Thu, 01 Jan 1970 00:00:00 GMT',
            max_age=0,
            samesite=settings.JWT_AUTH_SAMESITE,
            secure=settings.JWT_AUTH_SECURE,
        )
        response.set_cookie(
            key=settings.JWT_AUTH_REFRESH_COOKIE,
            value='',
            httponly=True,
            expires='Thu, 01 Jan 1970 00:00:00 GMT',
            max_age=0,
            samesite=settings.JWT_AUTH_SAMESITE,
            secure=settings.JWT_AUTH_SECURE,
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

        rotate_token(self.request)
        return response