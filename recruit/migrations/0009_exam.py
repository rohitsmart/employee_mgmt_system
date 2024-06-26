# Generated by Django 5.0.3 on 2024-04-17 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0008_result'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id',models.IntegerField(null=True)),
                ('candidateResponse', models.CharField(max_length=255)),
                ('correctResponse', models.CharField(max_length=255)),
                ('Date', models.DateField()),
                ('round', models.IntegerField(choices=[(1, 'Round 1'), (2, 'Round 2')],null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
                # ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruit.questions')),
                ('scheduler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruit.scheduler')),
            ],
        ),
    ]
