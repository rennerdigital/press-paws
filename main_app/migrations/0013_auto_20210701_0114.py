# Generated by Django 3.1.7 on 2021-07-01 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_auto_20210701_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='number_of_nights',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_owed',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
