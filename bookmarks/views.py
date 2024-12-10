from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Count
from rest_framework.response import Response
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


class BookmarkFolderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a folder.
    Includes bookmarks inside the folder in GET responses.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookmarkFolderSerializer
    queryset = BookmarkFolder.objects.annotate(
        bookmarks_count=Count('bookmarks')
    )

    def get(self, request, *args, **kwargs):
        # Fetch folder and its bookmarks
        folder = self.get_object()
        bookmarks = folder.bookmarks.all()  # Use related_name for easy reverse lookup
        data = {
            'folder': BookmarkFolderSerializer(folder).data,
            'bookmarks': BookmarkSerializer(bookmarks, many=True).data
        }
        return Response(data)


class BookmarksInFolder(generics.ListAPIView):
    """
    Fetch bookmarks inside a specific folder by folder ID.
    """
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        folder_id = self.kwargs.get('folder_id')
        return Bookmark.objects.filter(folder_id=folder_id, owner=self.request.user)


class BookmarkList(generics.ListCreateAPIView):
    """
    Lists all bookmarks for the authenticated user and allows new bookmark creation.
    """
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookmarkDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a specific bookmark by ID.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
