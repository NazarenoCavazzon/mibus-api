# Generated by Django 3.2.8 on 2021-10-11 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0036_alter_company_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='ticket_price',
            field=models.FloatField(blank=True, default=0),
        ),
    ]