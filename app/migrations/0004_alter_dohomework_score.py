# Generated by Django 4.2.7 on 2023-11-15 03:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_user_options_alter_homework_class_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dohomework',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
