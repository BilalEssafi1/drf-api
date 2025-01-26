from django.middleware.csrf import rotate_token
from .utils import clear_auth_cookies

class CookieCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for stale/invalid session
        if not request.user.is_authenticated and 'my-app-auth' in request.COOKIES:
            response = self.get_response(request)
            response = clear_auth_cookies(response)
            rotate_token(request)
            return response
        return self.get_response(request)