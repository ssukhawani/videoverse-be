# Generated by Django 5.0.7 on 2024-07-22 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoverse', '0003_alter_video_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
