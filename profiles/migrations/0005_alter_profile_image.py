# Generated by Django 5.1.3 on 2024-12-03 11:15

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_delete_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, default='../coffee', max_length=255, verbose_name='image'),
        ),
    ]
