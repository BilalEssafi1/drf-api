from rest_framework import serializers
from .models import BookmarkFolder, Bookmark
from posts.models import Post

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
    Serializer for bookmarks.
    Handles bookmark creation and validation with proper post relationship.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    post_title = serializers.ReadOnlyField(source='post.title')
    folder_name = serializers.ReadOnlyField(source='folder.name')
    post_id = serializers.ReadOnlyField(source='post.id')
    post_owner = serializers.ReadOnlyField(source='post.owner.username')
    post_image = serializers.ReadOnlyField(source='post.image.url')

    class Meta:
        model = Bookmark
        fields = [
            'id', 'owner', 
            'post', 'post_id', 'post_title', 'post_owner', 'post_image',
            'folder', 'folder_name', 
            'created_at'
        ]
        read_only_fields = ['owner']

    def to_representation(self, instance):
        """
        Customize the output representation of the bookmark
        Ensures post data is correctly included
        """
        representation = super().to_representation(instance)
        representation['post'] = {
            'id': instance.post.id,
            'title': instance.post.title,
            'owner': instance.post.owner.username,
            'image': instance.post.image.url if instance.post.image else None,
        }
        return representation

    def validate(self, data):
        """
        Validate bookmark data.
        Ensures required fields are present and no duplicates exist.
        Also validates that the post exists.
        """
        # Check required fields
        if not data.get('post'):
            raise serializers.ValidationError({
                'post': 'This field is required.'
            })
        
        if not data.get('folder'):
            raise serializers.ValidationError({
                'folder': 'This field is required.'
            })

        # Verify the post exists
        try:
            post = Post.objects.get(id=data['post'].id)
            data['post'] = post
        except Post.DoesNotExist:
            raise serializers.ValidationError({
                'post': 'Invalid post ID provided.'
            })

        # Check for duplicate bookmarks
        request = self.context.get('request')
        if request and request.user:
            existing = Bookmark.objects.filter(
                owner=request.user,
                post=data['post'],
                folder=data['folder']
            ).exists()
            if existing:
                raise serializers.ValidationError({
                    'detail': "You have already bookmarked this post in this folder."
                })

        return data
