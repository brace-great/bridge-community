# Generated by Django 4.0.3 on 2022-03-25 14:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0007_userinfo_email_alter_userinfo_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='birthday',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 25, 14, 44, 30, 880619, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]