# Generated by Django 3.2.8 on 2021-11-17 03:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rlcapp', '0017_auto_20211116_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='applications',
        ),
        migrations.AddField(
            model_name='applications',
            name='applicant',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Applicant'),
        ),
        migrations.AddField(
            model_name='progress_reports',
            name='remarks',
            field=models.TextField(blank=True, default='', verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='progress_reports',
            name='date_submitted',
            field=models.DateField(default=datetime.datetime(2021, 11, 17, 3, 46, 44, 172226, tzinfo=utc), verbose_name='Date Submitted'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='date_started',
            field=models.DateField(default=datetime.datetime(2021, 11, 17, 3, 46, 44, 172226, tzinfo=utc), verbose_name='Date Started'),
        ),
    ]
