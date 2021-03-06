# Generated by Django 3.2.7 on 2021-09-24 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0027_rename_busstop_busstops'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='busstops',
            name='address',
        ),
        migrations.RemoveField(
            model_name='busstops',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='busstops',
            name='lines',
        ),
        migrations.RemoveField(
            model_name='busstops',
            name='lng',
        ),
        migrations.RemoveField(
            model_name='busstops',
            name='name',
        ),
        migrations.RemoveField(
            model_name='busstops',
            name='subtitle',
        ),
        migrations.AddField(
            model_name='busstops',
            name='busStops',
            field=models.JSONField(null=True),
        ),
    ]
