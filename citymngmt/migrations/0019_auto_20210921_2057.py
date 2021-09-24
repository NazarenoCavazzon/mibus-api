# Generated by Django 3.2.7 on 2021-09-21 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0018_remove_line_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='line',
            old_name='zone_times',
            new_name='return_trip',
        ),
        migrations.AddField(
            model_name='line',
            name='round_trip',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='line',
            name='special_trip',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='line',
            name='zone',
            field=models.TextField(default=''),
        ),
    ]
