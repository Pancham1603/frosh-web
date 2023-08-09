# Generated by Django 4.2 on 2023-08-06 21:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_eventpass_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='booking_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eventslot',
            name='booking_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='eventpass',
            name='qr',
            field=models.URLField(validators=[django.core.validators.URLValidator]),
        ),
    ]
