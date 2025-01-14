from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import IntegrityError
from django.db.models import Count
from django.core.exceptions import ValidationError
from .models import BookmarkFolder, Bookmark
from .serializers import BookmarkFolderSerializer, BookmarkSerializer
from drf_api.permissions import IsOwnerOrReadOnly
import logging

logger = logging.getLogger(__name__)


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


class BookmarkFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific bookmark folder
    Only allows owners to modify their folders
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookmarkFolderSerializer
    queryset = BookmarkFolder.objects.all()

    def perform_update(self, serializer):
        """Ensure folder names remain unique per user"""
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError({"detail": "A folder with this name exists alreadya"})


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
        Override create method to handle bookmark creation with error handling
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except ValidationError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'detail': "You have already bookmarked this post in this folder."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        """Set the owner during bookmark creation"""
        serializer.save(owner=self.request.user)


class BookmarksInFolder(generics.ListAPIView):
    """
    Fetch bookmarks inside a specific folder by folder ID
    """
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter bookmarks by folder and owner
        """
        folder_id = self.kwargs.get('folder_id')
        return Bookmark.objects.select_related(
            'post',
            'post__owner',
            'folder'
        ).filter(
            folder_id=folder_id,
            owner=self.request.user
        ).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """
        Override list method to structure response properly
        """
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "results": serializer.data
            })
        except Exception as e:
            return Response(
                {'detail': 'Error retrieving bookmarks'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BookmarkDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a specific bookmark by ID
    Only allows owners to delete their bookmarks
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
