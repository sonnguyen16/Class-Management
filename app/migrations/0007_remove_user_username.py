# Generated by Django 4.2.7 on 2023-11-15 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_user_groups_remove_user_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
