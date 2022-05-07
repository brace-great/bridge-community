# Generated by Django 4.0.3 on 2022-04-06 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0028_discusswithtag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('content_type', models.CharField(max_length=100)),
                ('content_id', models.IntegerField()),
                ('content_text', models.IntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
