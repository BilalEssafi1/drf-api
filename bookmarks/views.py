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
        Includes enhanced error handling and proper owner assignment
        """
        try:
            serializer.save(owner=self.request.user)
        except ValidationError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'detail': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_serializer_context(self):
        """
        Add request to serializer context
        This ensures the serializer has access to the current user
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class BookmarksInFolder(generics.ListAPIView):
    """
    Fetch bookmarks inside a specific folder by folder ID.
    Allows users to view all bookmarks within a particular folder.
    """
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter bookmarks to only show those in the specified folder
        and owned by the current user
        """
        folder_id = self.kwargs.get('folder_id')
        return Bookmark.objects.filter(
            folder_id=folder_id, 
            owner=self.request.user
        )

class BookmarkDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a specific bookmark by ID.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
