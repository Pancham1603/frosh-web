# Generated by Django 4.2 on 2023-07-28 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_eventslot_slot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventslot',
            name='slot_id',
            field=models.CharField(primary_key=True, serialize=False, unique=True),
        ),
    ]
