# Generated by Django 3.0 on 2019-12-03 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191203_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mrange', models.IntegerField()),
                ('number', models.IntegerField()),
                ('normalized', models.FloatField()),
                ('alternatives', models.ManyToManyField(to='core.Alternative')),
                ('criterion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Criterion')),
            ],
        ),
    ]
