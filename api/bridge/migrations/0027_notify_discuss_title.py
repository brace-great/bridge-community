# Generated by Django 4.0.3 on 2022-04-03 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0026_remove_notify_text_notify_event_type_notify_from_who'),
    ]

    operations = [
        migrations.AddField(
            model_name='notify',
            name='discuss_title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
