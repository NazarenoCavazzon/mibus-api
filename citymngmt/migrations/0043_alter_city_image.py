# Generated by Django 3.2.8 on 2021-10-11 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0042_alter_city_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='city_images/'),
        ),
    ]