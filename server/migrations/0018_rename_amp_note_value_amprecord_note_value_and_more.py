# Generated by Django 5.1 on 2024-11-30 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0017_alter_amprecord_note_cumulative_layout_shift_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="amprecord",
            old_name="amp_note_value",
            new_name="note_value",
        ),
        migrations.RenameField(
            model_name="amprecord",
            old_name="amp_total_value",
            new_name="total_value",
        ),
        migrations.RenameField(
            model_name="amprecord",
            old_name="amp_video_value",
            new_name="video_value",
        ),
    ]
