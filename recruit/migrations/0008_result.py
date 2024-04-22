# Generated by Django 5.0.3 on 2024-04-17 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0007_scheduler'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=70)),
                ('date', models.DateField()),
                ('maximum', models.IntegerField()),
                ('obtained', models.IntegerField()),
                ('needed', models.IntegerField()),
                ('round', models.CharField(choices=[(1, 'Round 1'), (2, 'Round 2')], max_length=50)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
                # ('scheduler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruit.scheduler')),
            ],
        ),
    ]
