# Generated by Django 4.0.3 on 2022-04-02 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0022_alter_discusstag_discuss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='discuss',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bridge.discuss'),
        ),
    ]
