# Generated by Django 4.2.7 on 2023-11-16 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_homework_created_by_alter_class_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='invite_code',
            field=models.CharField(blank=True, default='DFWHfpXoRWriQxaWCjsqZY', max_length=30, null=True),
        ),
    ]
