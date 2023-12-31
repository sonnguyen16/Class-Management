# Generated by Django 4.2.7 on 2023-11-16 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_class_image_alter_class_invite_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='image',
            field=models.ImageField(blank=True, default='thump-1.png', null=True, upload_to='static/uploads/class'),
        ),
        migrations.AlterField(
            model_name='class',
            name='invite_code',
            field=models.CharField(blank=True, default='GjiXNnkVWA4pPQM59r7tG7', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='homework',
            name='image',
            field=models.ImageField(blank=True, default='thump-2.png', null=True, upload_to='static/uploads/homework'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='pic-1.jpg', null=True, upload_to='app/static/uploads/avatar'),
        ),
    ]
