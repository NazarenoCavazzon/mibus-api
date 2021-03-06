# Generated by Django 3.2.8 on 2021-10-30 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0046_auto_20211030_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='busstops',
            name='busStops',
        ),
        migrations.AddField(
            model_name='busstops',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='busstops',
            name='lng',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='busstops',
            name='name',
            field=models.TextField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='busstops',
            name='schedule',
            field=models.JSONField(null=True),
        ),
    ]
