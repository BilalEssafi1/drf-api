from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class BookmarkFolder(models.Model):
    """
    Folder model to organize bookmarked posts
    Allows users to create collections of bookmarks
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
    Allows users to save posts into specific folders

    Fields:
    - owner: The user who created the bookmark
    - post: The post being bookmarked
    - folder: The folder the bookmark belongs to
    - created_at: Timestamp of bookmark creation
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who created the bookmark"
    )
    post = models.ForeignKey(
        Post,
        related_name='bookmarks',
        on_delete=models.CASCADE,
        help_text="Post being bookmarked"
    )
    folder = models.ForeignKey(
        BookmarkFolder,
        related_name='bookmarks',
        on_delete=models.CASCADE,
        help_text="Folder containing the bookmark"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Time when bookmark was created"
    )

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'post', 'folder'],
                name='unique_bookmark',
                violation_error_message=(
                    "This post is already bookmarked in this folder."
                )
            )
        ]

    def __str__(self):
        return f"{self.owner} bookmarked {self.post} in {self.folder}"
