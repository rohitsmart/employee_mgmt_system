# Generated by Django 5.0.4 on 2024-05-04 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_emp_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='emp',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.empid'),
        ),
    ]
