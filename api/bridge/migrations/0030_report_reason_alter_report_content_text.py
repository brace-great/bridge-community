# Generated by Django 4.0.3 on 2022-04-06 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0029_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='reason',
            field=models.TextField(default='d'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='report',
            name='content_text',
            field=models.TextField(),
        ),
    ]
