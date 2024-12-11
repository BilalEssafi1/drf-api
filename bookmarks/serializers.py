from rest_framework import serializers
from .models import BookmarkFolder, Bookmark
from posts.models import Post

class BookmarkFolderSerializer(serializers.ModelSerializer):
   """
   Serializer for bookmark folders
   Includes count of bookmarks in each folder and basic folder information
   """
   owner = serializers.ReadOnlyField(source='owner.username')
   bookmarks_count = serializers.ReadOnlyField()

   class Meta:
       model = BookmarkFolder
       fields = [
           'id', 'owner', 'name', 'created_at', 
           'updated_at', 'bookmarks_count'
       ]

class BookmarkSerializer(serializers.ModelSerializer):
   """
   Serializer for bookmarks.
   Handles bookmark creation, validation and proper data representation
   with complete post relationship details.
   """

   owner = serializers.ReadOnlyField(source='owner.username')
   post_title = serializers.ReadOnlyField(source='post.title')
   post_id = serializers.ReadOnlyField(source='post.id')
   post_owner = serializers.ReadOnlyField(source='post.owner.username')
   post_image = serializers.ReadOnlyField(source='post.image.url')
   folder_name = serializers.ReadOnlyField(source='folder.name')

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
       Ensures all required post data is correctly included for the Post component
       """

       representation = super().to_representation(instance)
       representation['post'] = {
           'id': instance.post.id,
           'title': instance.post.title,
           'content': instance.post.content,
           'image': instance.post.image.url if instance.post.image else None,
           'created_at': instance.post.created_at,
           'updated_at': instance.post.updated_at,
           'owner': instance.post.owner.username,
           'profile_id': instance.post.owner.profile.id,
           'profile_image': instance.post.owner.profile.image.url,
           'likes_count': instance.post.likes.count(),
           'comments_count': instance.post.comment_set.count(),
           'like_id': None,
           'is_owner': False
       }
       
       return representation

   def validate(self, data):
       """
       Validate bookmark data before saving
       """

       if not data.get('post'):
           raise serializers.ValidationError({
               'post': 'This field is required.'
           })
       
       if not data.get('folder'):
           raise serializers.ValidationError({
               'folder': 'This field is required.'
           })

       try:
           post = Post.objects.get(id=data['post'].id)
           data['post'] = post
       except Post.DoesNotExist:
           raise serializers.ValidationError({
               'post': 'Invalid post ID provided.'
           })

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
