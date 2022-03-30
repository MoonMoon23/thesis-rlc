# Generated by Django 3.2.8 on 2021-11-17 05:03

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rlcapp', '0019_auto_20211117_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applications',
            name='projects',
        ),
        migrations.AddField(
            model_name='projects',
            name='application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='rlcapp.applications', verbose_name='Associated Application'),
        ),
        migrations.AlterField(
            model_name='progress_reports',
            name='date_submitted',
            field=models.DateField(default=datetime.datetime(2021, 11, 17, 5, 3, 38, 278760, tzinfo=utc), verbose_name='Date Submitted'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='date_started',
            field=models.DateField(default=datetime.datetime(2021, 11, 17, 5, 3, 38, 278760, tzinfo=utc), verbose_name='Date Started'),
        ),
    ]