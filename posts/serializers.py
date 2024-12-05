from rest_framework import serializers
from posts.models import Post, Tag
from likes.models import Like

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    Includes fields for post details, user interactions, and validation for image size.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    tags = serializers.SlugRelatedField(slug_field='name', queryset=Tag.objects.all(), many=True) 

    # Validation for image size, height, and width
    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096: 
            raise serializers.ValidationError('Image height larger than 4096px!')
        if value.image.width > 4096: 
            raise serializers.ValidationError('Image width larger than 4096px!')
        return value

    # Custom method to check if the current user is the owner of the post
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # Custom method to get the like ID for the current user, if they have liked the post
    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None

    # Dynamically calculate likes count by checking how many likes the post has
    def get_likes_count(self, obj):
        return obj.likes.count()

    # Dynamically calculate comments count by checking how many comments are associated with the post
    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 
            'profile_image', 'created_at', 'updated_at', 
            'title', 'content', 'image', 
            'like_id', 'likes_count', 'comments_count', 'tags',
        ]