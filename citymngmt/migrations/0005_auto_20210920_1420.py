# Generated by Django 3.2.7 on 2021-09-20 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0004_rename_user_id_city_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='color',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='company',
            name='password',
            field=models.TextField(default=''),
        ),
    ]
