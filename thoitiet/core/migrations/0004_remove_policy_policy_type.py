# Generated by Django 4.2 on 2025-04-23 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_id_district_district_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='policy_type',
        ),
    ]
