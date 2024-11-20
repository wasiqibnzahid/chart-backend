# Generated by Django 5.1 on 2024-11-19 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0010_localrecord_amp_note_value_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataUpload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.TextField(help_text="Paste your data here.")),
                (
                    "target_model",
                    models.CharField(
                        choices=[("record", "Record"), ("localrecord", "LocalRecord")],
                        default="record",
                        max_length=20,
                    ),
                ),
                (
                    "process_amp_values",
                    models.BooleanField(
                        choices=[(True, "Yes"), (False, "No")], default=False
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
