# Generated by Django 4.2 on 2023-07-28 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_eventpass_slot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpass',
            name='slot_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, to='events.eventslot'),
        ),
    ]
