# Generated by Django 4.2 on 2023-08-20 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoods', '0005_hood_member_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='hood',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
