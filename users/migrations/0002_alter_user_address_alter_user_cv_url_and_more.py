# Generated by Django 5.0.3 on 2024-04-23 06:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='cv_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='degree',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='emp_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.empid'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
