# Generated by Django 5.0.4 on 2024-05-04 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_user_degree_alter_user_firstname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
