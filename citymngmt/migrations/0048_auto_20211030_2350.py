# Generated by Django 3.2.8 on 2021-10-31 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0047_auto_20211030_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='busstops',
            name='saturday_schedule',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='busstops',
            name='sunday_schedule',
            field=models.JSONField(null=True),
        ),
    ]