# Generated by Django 4.0.3 on 2022-05-02 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leeds', '0002_userprofile_agent_organisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organisor',
            field=models.BooleanField(default=True),
        ),
    ]
