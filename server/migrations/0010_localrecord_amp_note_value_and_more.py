# Generated by Django 5.1 on 2024-11-14 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0009_auto_20241111_0411"),
    ]

    operations = [
        migrations.AddField(
            model_name="localrecord",
            name="amp_note_value",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="localrecord",
            name="amp_total_value",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="localrecord",
            name="amp_video_value",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="record",
            name="amp_note_value",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="record",
            name="amp_total_value",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="record",
            name="amp_video_value",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
