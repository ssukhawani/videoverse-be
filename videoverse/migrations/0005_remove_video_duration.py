# Generated by Django 5.0.7 on 2024-07-22 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videoverse', '0004_video_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='duration',
        ),
    ]
