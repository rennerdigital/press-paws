# Generated by Django 3.1.7 on 2021-06-30 01:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20210629_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date_from',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='date_to',
            field=models.DateField(default=datetime.date(2021, 6, 30)),
        ),
    ]