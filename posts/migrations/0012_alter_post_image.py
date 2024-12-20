# Generated by Django 5.1.4 on 2024-12-08 21:57

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='https://res.cloudinary.com/dsplumfvt/image/upload/v1733478884/green-apple_iubz3m.jpg', null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='posts/'),
        ),
    ]
