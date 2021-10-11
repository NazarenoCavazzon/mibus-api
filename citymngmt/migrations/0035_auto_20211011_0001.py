# Generated by Django 3.2.7 on 2021-10-11 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('citymngmt', '0034_alter_city_emergency_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='activated',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='city',
            name='emergency_phone',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='city',
            name='image',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.TextField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='city',
            name='polygon',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='status',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='city',
            name='ticket_price',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='city',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]