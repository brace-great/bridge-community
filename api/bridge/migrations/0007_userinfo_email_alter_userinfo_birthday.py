# Generated by Django 4.0.3 on 2022-03-25 14:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0006_alter_userinfo_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.CharField(default='f\x01', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='birthday',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 25, 14, 41, 25, 338370, tzinfo=utc)),
        ),
    ]
