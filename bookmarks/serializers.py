from rest_framework import serializers
from .models import BookmarkFolder, Bookmark

class BookmarkFolderSerializer(serializers.ModelSerializer):
    """
    Serializer for bookmark folders. Includes count of bookmarks in each folder.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    bookmarks_count = serializers.ReadOnlyField()

    class Meta:
        model = BookmarkFolder
        fields = ['id', 'owner', 'name', 'created_at', 'updated_at', 'bookmarks_count']


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer for bookmarks. Provides related post and folder details.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    post_title = serializers.ReadOnlyField(source='post.title')
    folder_name = serializers.ReadOnlyField(source='folder.name')

    class Meta:
        model = Bookmark
        fields = ['id', 'owner', 'post', 'post_title', 'folder', 'folder_name', 'created_at']