# Generated by Django 4.2 on 2023-08-11 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_hood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hood',
            field=models.CharField(blank=True, null=True),
        ),
    ]