# Generated by Django 4.0.3 on 2022-03-29 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0011_alter_userinfo_avatar_alter_userinfo_introduce'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('who', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('isread', models.BooleanField(default=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('isread', models.BooleanField(default=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
