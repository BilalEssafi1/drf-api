"""
Utility functions for authentication and cookie management
"""
from django.conf import settings

def clear_auth_cookies(response):
    """
    Comprehensive utility to clear all authentication and session cookies
    """
    # List all possible cookies that need to be cleared
    cookies_to_clear = [
        'csrftoken',
        'sessionid',
        'messages',
        'my-app-auth',
        'my-refresh-token',
        settings.JWT_AUTH_COOKIE,
        settings.JWT_AUTH_REFRESH_COOKIE
    ]
    
    # Standard cookie clearing options
    cookie_options = {
        'expires': 'Thu, 01 Jan 1970 00:00:00 GMT',
        'max_age': 0,
        'path': '/',
        'secure': True,
        'samesite': 'None',
        'httponly': True
    }
    
    # Clear each cookie with consistent settings
    for cookie in cookies_to_clear:
        response.set_cookie(
            key=cookie,
            value='',
            **cookie_options
        )
    
    return response

def get_auth_cookie_settings():
    """
    Returns standardized cookie settings for authentication cookies
    """
    return {
        'samesite': settings.JWT_AUTH_COOKIE_SAMESITE,
        'secure': settings.JWT_AUTH_COOKIE_SECURE,
        'httponly': True,
        'path': '/',
        'domain': None  # Let browser determine domain
    }
