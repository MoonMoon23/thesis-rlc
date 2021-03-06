# Generated by Django 3.2.8 on 2021-11-16 04:06

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rlcapp', '0011_auto_20211116_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress_reports',
            name='date_submitted',
            field=models.DateField(default=datetime.datetime(2021, 11, 16, 4, 6, 35, 467259, tzinfo=utc), verbose_name='Date Submitted'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='date_started',
            field=models.DateField(default=datetime.datetime(2021, 11, 16, 4, 6, 35, 467259, tzinfo=utc), verbose_name='Date Started'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='progress_report',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='rlcapp.progress_reports', verbose_name='Associated Progress Report'),
        ),
    ]
