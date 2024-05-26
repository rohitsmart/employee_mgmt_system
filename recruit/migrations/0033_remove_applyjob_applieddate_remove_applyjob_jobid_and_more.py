# Generated by Django 5.0.4 on 2024-05-26 03:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0032_rename_jobid_applyjob_jobid_applyjob_applieddate_and_more'),
        ('users', '0023_remove_empmodule_modulekey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applyjob',
            name='appliedDate',
        ),
        migrations.RemoveField(
            model_name='applyjob',
            name='jobId',
        ),
        migrations.RemoveField(
            model_name='applyjob',
            name='passingYear',
        ),
        migrations.AddField(
            model_name='applyjob',
            name='applied_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='applyjob',
            name='job_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='applyjob',
            name='passing_year',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='qualification',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='applyjob',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='users.user'),
        ),
        migrations.AlterField(
            model_name='applyjob',
            name='experience',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='applyjob',
            name='marks',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='applyjob',
            name='qualification',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applyjob',
            name='skills',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='applyjob',
            name='status',
            field=models.CharField(choices=[('Applied', 'Applied'), ('In Review', 'In Review'), ('Interviewed', 'Interviewed'), ('Offered', 'Offered'), ('Rejected', 'Rejected')], max_length=20, null=True),
        ),
    ]
