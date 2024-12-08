from django.db import models
from django.db.models.signals import post_save
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='profiles/', 
        blank=True, null=True, 
        default='https://res.cloudinary.com/dsplumfvt/image/upload/v1733478884/green-apple_iubz3m.jpg',
        storage=MediaCloudinaryStorage()) 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User) 