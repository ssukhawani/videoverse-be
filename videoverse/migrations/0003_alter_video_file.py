# Generated by Django 5.0.7 on 2024-07-21 14:18

import videoverse.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoverse', '0002_alter_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.FileField(upload_to=videoverse.models.user_directory_path),
        ),
    ]