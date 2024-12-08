# Generated by Django 5.1.4 on 2024-12-08 22:04

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='green-apple_iubz3m', null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='profiles/'),
        ),
    ]