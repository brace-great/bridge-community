# Generated by Django 4.0.3 on 2022-04-01 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0019_remove_discusstag_discuss_id_discusstag_discuss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discusstag',
            name='discuss',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='bridge.discuss'),
        ),
    ]
