# Generated by Django 3.0 on 2019-12-23 13:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20191223_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterion',
            name='weight',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
