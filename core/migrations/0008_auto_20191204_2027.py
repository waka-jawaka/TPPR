# Generated by Django 3.0 on 2019-12-04 20:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20191204_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='normalized',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='mark',
            name='number',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
