# Generated by Django 3.2.9 on 2021-12-13 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0049_city_position'),
    ]

    operations = [
        migrations.RenameField(
            model_name='busstops',
            old_name='lng',
            new_name='lon',
        ),
        migrations.AddField(
            model_name='busstops',
            name='direction',
            field=models.TextField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='busstops',
            name='order_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='busstops',
            name='subtitle',
            field=models.TextField(blank=True, max_length=50),
        ),
    ]
