# Generated by Django 3.2.7 on 2021-09-21 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citymngmt', '0012_alter_company_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyrelations',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
