from rest_framework import serializers
from posts.models import Post, Tag
from likes.models import Like
import re


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    Includes validation for images and dynamic user-generated hashtags.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    # Renamed field with help text
    add_hashtags = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text=(
            "Add words only, separated by commas (e.g., nature, travel, food)"
        )
    )

    # For output: return list of tag names
    tags = serializers.SerializerMethodField()

    def validate_add_hashtags(self, value):
        """
        Validate that hashtags contain only letters, numbers, and underscores
        """
        if value:
            tags = [tag.strip() for tag in value.split(',')]
            for tag in tags:
                if not re.match(r'^[\w]+$', tag):
                    raise serializers.ValidationError(
                        f"'{tag}' is not valid. Please use only "
                        "letters, numbers, and underscores."
                    )
        return value

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:  # 2MB size limit
            raise serializers.ValidationError(
                "Image size larger than 2MB!"
            )
        if value.image.height > 4096:  # Max height 4096px
            raise serializers.ValidationError(
                "Image height larger than 4096px!"
            )
        if value.image.width > 4096:  # Max width 4096px
            raise serializers.ValidationError(
                "Image width larger than 4096px!"
            )
        return value

    def create(self, validated_data):
        tags_input = validated_data.pop('add_hashtags', '')
        tag_names = self.extract_hashtags(tags_input)

        post = Post.objects.create(**validated_data)

        # Create or get tags and associate them with the post
        for tag_name in tag_names:
            # Remove the # symbol when storing in database
            clean_tag_name = tag_name.lstrip('#')
            tag, created = Tag.objects.get_or_create(name=clean_tag_name)
            post.tags.add(tag)

        return post

    def extract_hashtags(self, tags):
        if tags:
            return [
                f"#{tag.strip()}"
                for tag in tags.split(',')
                if tag.strip()
            ]
        return []

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None

    def get_tags(self, obj):
        """
        Return list of tag names with # symbol for the post
        """
        return [f"#{tag.name}" for tag in obj.tags.all()]

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'title', 'content', 'image',
            'created_at', 'updated_at', 'like_id',
            'likes_count', 'comments_count',
            'add_hashtags', 'tags',
        ]
