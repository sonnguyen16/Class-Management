# Generated by Django 4.2.7 on 2023-11-16 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_class_invite_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='invite_code',
            field=models.CharField(blank=True, default='QW57LCtuWSmTbWyKNaqxMe', max_length=30, null=True),
        ),
    ]
