# Generated by Django 4.2.7 on 2023-11-15 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_class_invite_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='invite_code',
            field=models.CharField(blank=True, default='Cjbr2tWeUEoCEVP94oFkqU', max_length=30, null=True),
        ),
    ]
