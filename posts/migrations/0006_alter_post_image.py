# Generated by Django 5.1.3 on 2024-12-03 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='../coffee', upload_to='images/'),
        ),
    ]
