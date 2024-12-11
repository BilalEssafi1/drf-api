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
    Serializer for the Bookmark model
    Handles creation and validation of bookmarks
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    post_title = serializers.ReadOnlyField(source='post.title')
    folder_name = serializers.ReadOnlyField(source='folder.name')

    class Meta:
        model = Bookmark
        fields = [
            'id', 'owner', 'post', 'post_title', 
            'folder', 'folder_name', 'created_at'
        ]
        # NEW: Added validator to prevent duplicate bookmarks
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Bookmark.objects.all(),
                fields=['owner', 'post', 'folder'],
                message="You have already bookmarked this post in this folder."
            )
        ]

    def validate(self, data):
        """
        Validates that both post and folder are provided
        """
        if not data.get('post'):
            raise serializers.ValidationError({
                'post': 'This field is required.'
            })
        if not data.get('folder'):
            raise serializers.ValidationError({
                'folder': 'This field is required.'
            })
        return data

    def create(self, validated_data):
        """
        Creates and returns a new Bookmark instance
        Includes additional validation
        """
        try:
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError({
                'detail': f'Error creating bookmark: {str(e)}'
            })