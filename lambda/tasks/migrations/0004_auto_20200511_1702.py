# Generated by Django 3.0.5 on 2020-05-11 16:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20200508_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_due',
            field=models.DateField(default=datetime.date(2020, 5, 15)),
            preserve_default=False,
        ),
    ]
