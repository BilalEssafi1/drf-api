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
    Lists all bookmark folders for the authenticated user
    Allows creation of new folders
    """
    serializer_class = BookmarkFolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get all folders for the current user with bookmark counts"""
        return BookmarkFolder.objects.filter(owner=self.request.user).annotate(
            bookmarks_count=Count('bookmarks')
        )

    def perform_create(self, serializer):
        """Create new folder with current user as owner"""
        serializer.save(owner=self.request.user)

class BookmarkList(generics.ListCreateAPIView):
    """
    Lists all bookmarks for the authenticated user
    Allows creation of new bookmarks
    """
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get all bookmarks for the current user"""
        return Bookmark.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override create method to handle owner field and provide better error handling
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        """Set the owner during bookmark creation"""
        serializer.save(owner=self.request.user)

class BookmarksInFolder(generics.ListAPIView):
    """
    Fetch bookmarks inside a specific folder by folder ID.
    Allows users to view all bookmarks within a particular folder.
    Includes full post data for each bookmark.
    """
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter bookmarks to only show those in the specified folder
        and owned by the current user.
        Uses select_related to efficiently fetch related post data.
        """
        folder_id = self.kwargs.get('folder_id')
        return Bookmark.objects.select_related(
            'post',
            'owner',
            'folder'
        ).filter(
            folder_id=folder_id,
            owner=self.request.user
        )

class BookmarkDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a specific bookmark by ID
    Only allows owners to delete their bookmarks
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

