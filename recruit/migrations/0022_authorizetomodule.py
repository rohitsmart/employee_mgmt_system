# Generated by Django 5.0.4 on 2024-05-04 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0021_merge_20240504_1715'),
        ('users', '0006_user_emp'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizeToModule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.empmodule')),
            ],
        ),
    ]
