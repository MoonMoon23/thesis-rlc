# Generated by Django 3.2.8 on 2022-03-23 06:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rlcapp', '0029_auto_20220323_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='approved_by',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='applications',
            name='checked_by',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='progress_reports',
            name='date_submitted',
            field=models.DateField(default=datetime.datetime(2022, 3, 23, 6, 9, 23, 421873, tzinfo=utc), verbose_name='Date Submitted'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='date_started',
            field=models.DateField(default=datetime.datetime(2022, 3, 23, 6, 9, 23, 421873, tzinfo=utc), verbose_name='Date Started'),
        ),
    ]