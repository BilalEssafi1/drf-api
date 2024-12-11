from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Count
from django.core.exceptions import ValidationError
from .models import BookmarkFolder, Bookmark
from .serializers import BookmarkFolderSerializer, BookmarkSerializer
from drf_api.permissions import IsOwnerOrReadOnly

class BookmarkFolderList(generics.ListCreateAPIView):
    """
    Lists all bookmark folders for the authenticated user and allows creation of new folders.
    """
    serializer_class = BookmarkFolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookmarkFolder.objects.filter(owner=self.request.user).annotate(
            bookmarks_count=Count('bookmarks')
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BookmarkList(generics.ListCreateAPIView):
    """
    Lists all bookmarks for the authenticated user and allows new bookmark creation.
    """
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter bookmarks to show only those owned by the current user
        """
        return Bookmark.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new bookmark
        """
        try:
            # Attempt to save the bookmark
            serializer.save(owner=self.request.user)
        except ValidationError as e:
            # Handle validation errors
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Handle other errors
            return Response(
                {'detail': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BookmarkDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a specific bookmark by ID.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
