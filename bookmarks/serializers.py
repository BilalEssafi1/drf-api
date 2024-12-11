from rest_framework import serializers
from .models import BookmarkFolder, Bookmark

class BookmarkFolderSerializer(serializers.ModelSerializer):
    """
    Serializer for bookmark folders
    Includes count of bookmarks in each folder
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    bookmarks_count = serializers.ReadOnlyField()

    class Meta:
        model = BookmarkFolder
        fields = ['id', 'owner', 'name', 'created_at', 'updated_at', 'bookmarks_count']

class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer for bookmarks. Provides comprehensive post and folder details.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    post_title = serializers.ReadOnlyField(source='post.title')
    post_content = serializers.ReadOnlyField(source='post.content')
    post_image = serializers.ReadOnlyField(source='post.image')
    post_owner = serializers.ReadOnlyField(source='post.owner.username')
    folder_name = serializers.ReadOnlyField(source='folder.name')

    class Meta:
        model = Bookmark
        fields = [
            'id', 'owner', 
            'post', 'post_title', 'post_content', 'post_image', 'post_owner',
            'folder', 'folder_name', 
            'created_at'
        ]
        read_only_fields = ['owner']

    def validate(self, data):
        """
        Validate the bookmark data
        """
        if not data.get('post'):
            raise serializers.ValidationError({
                'post': 'This field is required.'
            })
        if not data.get('folder'):
            raise serializers.ValidationError({
                'folder': 'This field is required.'
            })

        # Check for duplicate bookmarks
        request = self.context.get('request')
        if request and request.user:
            existing = Bookmark.objects.filter(
                owner=request.user,
                post=data.get('post'),
                folder=data.get('folder')
            ).exists()
            if existing:
                raise serializers.ValidationError(
                    "You have already bookmarked this post in this folder."
                )

        return data
