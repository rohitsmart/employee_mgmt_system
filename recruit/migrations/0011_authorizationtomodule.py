# Generated by Django 5.0.3 on 2024-04-17 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0010_authorizationtoemployee'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizationToModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module_authorizations', to='users.user')),
            ],
        ),
    ]