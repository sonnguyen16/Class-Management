# Generated by Django 4.2.7 on 2023-11-15 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_class_invite_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='opencv_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='invite_code',
            field=models.CharField(blank=True, default='AM8GFTUNbQijf8vXn6RNpe', max_length=30, null=True),
        ),
    ]
