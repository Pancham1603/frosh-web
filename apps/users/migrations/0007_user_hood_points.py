# Generated by Django 4.2 on 2023-08-20 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_hood'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hood_points',
            field=models.IntegerField(default=0),
        ),
    ]