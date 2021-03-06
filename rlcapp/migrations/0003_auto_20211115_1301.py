# Generated by Django 3.2.8 on 2021-11-15 05:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rlcapp', '0002_alter_applications_date_started'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='date_started',
            field=models.DateField(default=datetime.datetime(2021, 11, 15, 5, 1, 58, 388064, tzinfo=utc), verbose_name='Date Started'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='designation',
            field=models.CharField(blank=True, choices=[('INST', 'Instructor'), ('ASCP', 'Associate Professor'), ('ASTP', 'Assistant Professor'), ('PROF', 'Professor')], default='INST', max_length=4, null=True),
        ),
    ]
