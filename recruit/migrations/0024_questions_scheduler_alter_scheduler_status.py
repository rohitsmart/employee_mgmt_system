# Generated by Django 5.0.4 on 2024-05-14 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0023_merge_0021_merge_20240502_1201_0022_authorizetomodule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduler',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('attempted', 'attempted')], max_length=15),
        ),
    ]