# Generated by Django 5.0.7 on 2024-07-22 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoverse', '0008_mergedvideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='mergedvideo',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=False,
        ),
    ]
