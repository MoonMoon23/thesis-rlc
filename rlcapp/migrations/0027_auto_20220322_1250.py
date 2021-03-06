# Generated by Django 3.2.8 on 2022-03-22 04:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rlcapp', '0026_auto_20211202_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='schoolyear',
            field=models.IntegerField(choices=[(2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)], default=2022, verbose_name='Schoolyear'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'DRAFT'), ('PENDING DEPARTMENT APPROVAL', 'PENDING DEPARTMENT APPROVAL'), ('FOR REVISION', 'FOR REVISION'), ('PENDING COLLEGE APPROVAL', 'PENDING COLLEGE APPROVAL'), ('APPROVED', 'APPROVED'), ('EXTENDED', 'EXTENDED'), ('COMPLETED', 'COMPLETED')], default='DRAFT', max_length=90),
        ),
        migrations.AlterField(
            model_name='progress_reports',
            name='date_submitted',
            field=models.DateField(default=datetime.datetime(2022, 3, 22, 4, 50, 14, 907361, tzinfo=utc), verbose_name='Date Submitted'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='date_started',
            field=models.DateField(default=datetime.datetime(2022, 3, 22, 4, 50, 14, 891771, tzinfo=utc), verbose_name='Date Started'),
        ),
    ]
