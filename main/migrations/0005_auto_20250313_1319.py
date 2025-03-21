# Generated by Django 5.1.7 on 2025-03-13 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_appointment_created_at_appointment_updated_at'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                    ALTER TABLE main_appointment
                    ALTER COLUMN service_id TYPE bigint USING service_id::bigint;
                """,
            reverse_sql="""
                    ALTER TABLE main_appointment
                    ALTER COLUMN service_id TYPE character varying USING service_id::text;
                """
        ),
    ]
