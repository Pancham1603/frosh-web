# Generated by Django 4.2 on 2023-08-20 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoods', '0006_hood_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='hood',
            name='is_booking',
            field=models.BooleanField(default=True),
        ),
    ]
