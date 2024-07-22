# Generated by Django 5.0.7 on 2024-07-21 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userlimit_unit_alter_userlimit_limit_value'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userlimit',
            constraint=models.UniqueConstraint(fields=('user', 'limit_name'), name='unique_user_limit'),
        ),
    ]