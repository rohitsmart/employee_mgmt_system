# Generated by Django 5.0.3 on 2024-04-11 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('module', '0001_initial'),
        ('project', '0001_initial'),
        ('task', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_to',models.CharField(max_length=30)),
                ('assigned_by', models.CharField(max_length=30)),
                ('assign_date', models.DateField()),
                ('deadline', models.DateField()),
                ('status', models.CharField(max_length=30)),
                ('comment', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task')),
                # ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]