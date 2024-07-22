# Generated by Django 5.0.7 on 2024-07-22 18:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoverse', '0005_remove_video_duration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrimmedVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=255)),
                ('file_size', models.PositiveIntegerField()),
                ('start_time', models.FloatField()),
                ('end_time', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('original_video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videoverse.video')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]