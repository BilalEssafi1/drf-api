from django.db.models import Count
from rest_framework import generics, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.middleware.csrf import rotate_token
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer
from django.core.exceptions import ValidationError
from django.conf import settings

JWT_AUTH_COOKIE = getattr(settings, 'JWT_AUTH_COOKIE', None)
JWT_AUTH_REFRESH_COOKIE = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
JWT_AUTH_SAMESITE = getattr(settings, 'JWT_AUTH_SAMESITE', 'None')
JWT_AUTH_SECURE = getattr(settings, 'JWT_AUTH_SECURE', True)

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = instance.owner
            
            # Delete profile and user
            instance.delete()
            user.delete()
            
            # Create response with cookie cleanup
            response = Response(status=status.HTTP_204_NO_CONTENT)
            
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
            
        except Exception as e:
            raise ValidationError({"detail": "Error deleting account. Please try again."})
