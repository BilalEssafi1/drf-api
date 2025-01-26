from django.middleware.csrf import rotate_token
from django.contrib.auth import logout

class TokenValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response