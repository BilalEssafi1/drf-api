from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from django.middleware.csrf import rotate_token
from rest_framework import status
from .utils import clear_auth_cookies


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

        # Use unified cookie clearing utility
        response = clear_auth_cookies(response)
        rotate_token(request)
        return response
