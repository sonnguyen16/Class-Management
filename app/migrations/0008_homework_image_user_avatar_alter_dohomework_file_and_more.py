# Generated by Django 4.2.7 on 2023-11-15 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='image',
            field=models.ImageField(blank=True, default='app/static/images/thump-1.png', null=True, upload_to='app/static/uploads/homework'),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='app/static/images/pic-1.jpg', null=True, upload_to='app/static/uploads/avatar'),
        ),
        migrations.AlterField(
            model_name='dohomework',
            name='file',
            field=models.FileField(upload_to='app/static/uploads/homework'),
        ),
        migrations.AlterField(
            model_name='homework',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='app/static/uploads/homework'),
        ),
    ]
