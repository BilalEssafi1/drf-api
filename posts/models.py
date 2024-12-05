from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    """
    Tag model to categorize posts into sustainability-related topics.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Post model for user-generated content.
    Includes tags for categorization, a shareable URL, and an image (with default).
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    shareable_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True, default='../coffee') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_shareable_url(self):
        """
        Generates a unique shareable URL for the post.
        """
        from django.utils.crypto import get_random_string
        unique_id = get_random_string(8)
        self.shareable_url = f"https://ecosphere.com/posts/{unique_id}"
        self.save()

    def __str__(self):
        return self.title