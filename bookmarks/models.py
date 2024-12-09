from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.

class BookmarkFolder(models.Model):
    """
    Folder model to organize bookmarked posts
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['owner', 'name']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s folder: {self.name}"

class Bookmark(models.Model):
    """
    Bookmark model for saving posts
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='bookmarks', on_delete=models.CASCADE)
    folder = models.ForeignKey(BookmarkFolder, related_name='bookmarks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'post', 'folder']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner} bookmarked {self.post} in {self.folder}"