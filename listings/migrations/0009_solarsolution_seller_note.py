# Generated by Django 5.1.1 on 2024-10-30 15:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_rename_fire_extinguisher_included_service_hse_equipment_included_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solarsolution',
            name='seller_note',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(1000)]),
        ),
    ]
