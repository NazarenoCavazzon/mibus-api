# Generated by Django 3.2.7 on 2021-09-23 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0021_citysession'),
    ]

    operations = [
        migrations.RenameField(
            model_name='line',
            old_name='special_trip',
            new_name='special_return_trip',
        ),
        migrations.AddField(
            model_name='line',
            name='special_round_trip',
            field=models.TextField(default=''),
        ),
    ]