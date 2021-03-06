# Generated by Django 3.2.8 on 2021-11-16 05:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rlcapp', '0013_auto_20211116_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='signature',
        ),
        migrations.AddField(
            model_name='faculty',
            name='remarks',
            field=models.TextField(blank=True, default='', verbose_name='Remarks'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=10, verbose_name='Faculty Status'),
        ),
        migrations.AlterField(
            model_name='progress_reports',
            name='date_submitted',
            field=models.DateField(default=datetime.datetime(2021, 11, 16, 5, 8, 30, 490004, tzinfo=utc), verbose_name='Date Submitted'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='date_started',
            field=models.DateField(default=datetime.datetime(2021, 11, 16, 5, 8, 30, 490004, tzinfo=utc), verbose_name='Date Started'),
        ),
    ]
