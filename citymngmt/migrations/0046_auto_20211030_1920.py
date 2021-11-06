# Generated by Django 3.2.8 on 2021-10-30 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0045_rename_company_line_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='line',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='line',
            name='zone_times',
        ),
        migrations.AddField(
            model_name='busstops',
            name='line',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='citymngmt.line'),
        ),
    ]
