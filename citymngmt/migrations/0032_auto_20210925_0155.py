# Generated by Django 3.2.7 on 2021-09-25 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0031_line_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='emergency_phone',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='city',
            name='ticket_price',
            field=models.FloatField(default=0.0),
        ),
    ]
